import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import json
import os

# 1. Setup Kid-friendly styling and Page Config
st.set_page_config(page_title="Eco Lunch Scanner 🌍", page_icon="🥪", layout="wide")

st.markdown("""
<style>
    /* Fun title styling */
    h1, h2, h3 {
        color: #ff6b6b !important;
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Marker Felt', sans-serif !important;
    }
    
    /* Card style for the results */
    .metric-card {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center;
        margin: 10px;
        border: 4px solid #4ecdc4;
        color: #2c3e50; /* Ensure text inside the card is always readable */
    }
    
    .metric-card h3 {
        color: #34495e !important;
    }
    
    .metric-card p {
        color: #7f8c8d;
        font-weight: bold;
    }
    
    .eco-score-high { color: #2ecc71 !important; font-size: 3em !important; margin: 10px 0; }
    .eco-score-medium { color: #f1c40f !important; font-size: 3em !important; margin: 10px 0; }
    .eco-score-low { color: #e74c3c !important; font-size: 3em !important; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# 2. Data Logic: Load or initialize food data mapping
DATA_FILE = "food_data.json"

def load_food_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        default_data = {
            "Apple": {"water_l": 70, "carbon_kg": 0.04, "eco_score": 95},
            "Burger": {"water_l": 2400, "carbon_kg": 2.50, "eco_score": 20},
            "Banana": {"water_l": 160, "carbon_kg": 0.11, "eco_score": 85},
            "Pizza": {"water_l": 1200, "carbon_kg": 1.50, "eco_score": 40},
            "Salad": {"water_l": 150, "carbon_kg": 0.20, "eco_score": 90},
            "Background": {"water_l": 0, "carbon_kg": 0.00, "eco_score": 0}
        }
        with open(DATA_FILE, "w") as f:
            json.dump(default_data, f, indent=4)
        return default_data

def save_food_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

FOOD_DATA = load_food_data()

# Helper to get available models
def get_available_models():
    models_dir = "models"
    if not os.path.exists(models_dir):
        return []
    
    available_models = []
    for item in os.listdir(models_dir):
        item_path = os.path.join(models_dir, item)
        if os.path.isdir(item_path):
            if os.path.exists(os.path.join(item_path, "model_unquant.tflite")) and \
               os.path.exists(os.path.join(item_path, "labels.txt")):
                available_models.append(item)
    return sorted(available_models)

# 3. Load the pre-trained model and labels
@st.cache_resource
def load_model_and_labels(model_dir):
    try:
        model_path = os.path.join("models", model_dir, "model_unquant.tflite")
        labels_path = os.path.join("models", model_dir, "labels.txt")
        # Load TFLite model and allocate tensors
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        with open(labels_path, "r") as f:
            # Teachable Machine labels usually look like "0 Apple" or just "Apple"
            labels = [line.strip().split(" ", 1)[1] if " " in line else line.strip() for line in f.readlines()]
        return interpreter, labels
    except Exception as e:
        return None, None

# 4. Computer Vision: Preprocess frame for the Keras model
def preprocess_frame(frame):
    # Keras models typically expect 224x224 RGB image
    img = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
    img_array = np.asarray(img, dtype=np.float32)
    # Normalize the image to [-1, 1]
    normalized_image_array = (img_array / 127.5) - 1.0
    # Expand dimensions to match model input shape (1, 224, 224, 3)
    data = np.expand_dims(normalized_image_array, axis=0)
    return data

# Navigation Sidebar
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Go to:", ["Scanner Mode 📷", "Admin Dashboard ⚙️"])

if app_mode == "Scanner Mode 📷":
    st.title("🌱 Eco Lunch Scanner! 🥪")
    st.markdown("<h3 style='text-align: center; color: #4ecdc4;'>Let's see how earth-friendly your food is!</h3>", unsafe_allow_html=True)
    
    available_models = get_available_models()
    if not available_models:
        st.error("⚠️ No models found! Please create a folder in `models/` and add your `model_unquant.tflite` and `labels.txt` files.")
        st.stop()
        
    selected_model_dir = st.selectbox("🧠 Select AI Model:", available_models)
    model, labels = load_model_and_labels(selected_model_dir)
        
    # 5. UI/Dashboard Layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📸 Camera Feed")
        # Streamlit's native camera input creates a built-in "Take Photo" button
        picture = st.camera_input("Take a picture to scan your food! 🎥")

    with col2:
        st.markdown("### 🌍 Eco Results")
        results_placeholder = st.empty()
        
        if picture:
            # Convert the uploaded picture to a numpy array for OpenCV/TFLite
            # Ensure it's in RGB format to avoid 4-channel broadcast errors
            img = Image.open(picture).convert("RGB")
            frame_rgb = np.array(img)
            
            # Prevent false positives on black/empty images
            if np.mean(frame_rgb) < 15 or np.std(frame_rgb) < 5:
                with results_placeholder.container():
                    st.markdown("""
                    <div class="metric-card">
                        <h3>Oops! I can't see anything! 🌑</h3>
                        <p style="color: gray;">It looks like the camera is covered or the picture is too dark.<br>Try again in better lighting!</p>
                    </div>
                    """, unsafe_allow_html=True)
            # Perform prediction if model is loaded
            elif model is not None and labels is not None:
                processed_data = preprocess_frame(frame_rgb)
                
                # TFLite Inference
                input_details = model.get_input_details()
                output_details = model.get_output_details()
                
                model.set_tensor(input_details[0]['index'], processed_data)
                model.invoke()
                prediction = model.get_tensor(output_details[0]['index'])
                
                index = np.argmax(prediction)
                class_name = labels[index]
                confidence_score = prediction[0][index]
                
                # Check if the AI thinks there is no food in the picture
                if class_name == "Background":
                    with results_placeholder.container():
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>Looking for food... 👀</h3>
                            <p style="color: gray;">I don't see any food in this picture!<br>Confidence: {confidence_score*100:.0f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                # Update results dynamically if confidence is high and it's a known food
                elif confidence_score > 0.40 and class_name in FOOD_DATA:
                    stats = FOOD_DATA[class_name]
                    
                    # Determine Eco Score color class
                    if stats['eco_score'] > 70:
                        score_class = "eco-score-high"
                    elif stats['eco_score'] > 40:
                        score_class = "eco-score-medium"
                    else:
                        score_class = "eco-score-low"
                        
                    with results_placeholder.container():
                        st.markdown(f"""
                        <div class="metric-card">
                            <h2>{class_name} 🍽️</h2>
                            <p>I'm {confidence_score*100:.0f}% sure!</p>
                            <hr>
                            <h3>💧 Water Usage: <br>{stats['water_l']} Liters</h3>
                            <h3>💨 Carbon Footprint: <br>{stats['carbon_kg']} kg CO2</h3>
                            <h1 class="{score_class}">
                                Eco Score: {stats['eco_score']}/100
                            </h1>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    with results_placeholder.container():
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>Hmm... I'm not sure what that is! 🤔</h3>
                            <p style="color: gray;">My best guess: {class_name} ({confidence_score*100:.0f}%)</p>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            # Show a placeholder graphic/text when no picture is taken yet
            with results_placeholder.container():
                st.markdown("""
                <div class="metric-card">
                    <h2>Waiting for a picture...</h2>
                    <p>Click 'Take Photo' on the camera to scan!</p>
                </div>
                """, unsafe_allow_html=True)

elif app_mode == "Admin Dashboard ⚙️":
    st.title("⚙️ Admin Dashboard")
    st.markdown("Use this panel to teach the app the environmental impact of **new foods** after you've trained them in Teachable Machine!")
    
    st.markdown("### 1. Update Food Database")
    st.markdown("Add a new food item exactly as you named it in your Teachable Machine class.")
    
    with st.form("add_food_form"):
        new_name = st.text_input("Food Name (e.g., 'Carrot')")
        colA, colB, colC = st.columns(3)
        with colA:
            new_water = st.number_input("Water Usage (Liters)", min_value=0, value=50)
        with colB:
            new_carbon = st.number_input("Carbon Footprint (kg CO2)", min_value=0.0, value=0.1, step=0.1)
        with colC:
            new_eco = st.number_input("Eco Score (0-100)", min_value=0, max_value=100, value=80)
            
        submitted = st.form_submit_button("Add to Database 💾")
        if submitted:
            if new_name:
                FOOD_DATA[new_name] = {
                    "water_l": new_water,
                    "carbon_kg": new_carbon,
                    "eco_score": new_eco
                }
                save_food_data(FOOD_DATA)
                st.success(f"✅ Successfully added '{new_name}' to the database!")
            else:
                st.error("Please enter a valid Food Name.")
                
    st.markdown("#### Current Database")
    st.json(FOOD_DATA)
    
    st.markdown("---")
    st.markdown("### 2. Add New AI Models")
    st.info("""
    **To use multiple AI models for different categories (e.g., 'Fruits', 'Drinks'):**
    1. Go to [Google Teachable Machine](https://teachablemachine.withgoogle.com/).
    2. Train your new model (don't forget a 'Background' class!).
    3. Export as **TensorFlow Lite (Floating point)**.
    4. Create a new folder inside the `models/` directory (e.g., `models/drinks/`).
    5. Extract your downloaded `model_unquant.tflite` and `labels.txt` into that new folder.
    6. Refresh the app, and you can now select it from the dropdown in Scanner Mode!
    """)
