# 🌱 Eco Lunch Scanner! 🥪

Welcome to the **Eco Lunch Scanner** — an educational, kid-friendly AI application designed to teach children about the environmental impact of the foods they eat every day! 

By simply holding a food item up to the camera and clicking "Take Photo", this app uses a powerful Computer Vision model to identify the food and instantly display its **Water Usage**, **Carbon Footprint**, and an overall **Eco Score** (0-100).

---

## 🌟 Features

- **📸 Native Camera Integration**: A seamless, easy-to-use "Take Photo" interface that works flawlessly in the browser.
- **🧠 Multi-Model AI Architecture**: Switch seamlessly between different TensorFlow Lite AI models (e.g., "Fruits", "Junk Food") using a simple dropdown menu.
- **⚙️ Admin Dashboard**: A built-in control panel that allows teachers or parents to dynamically add new food items and their environmental statistics to the local JSON database without touching any code!
- **🎨 Kid-Friendly UI**: A vibrant, color-coded interface designed with Streamlit that makes learning about sustainability fun and visually engaging.

---

## 🚀 How to Run Locally

### Prerequisites
Make sure you have Python 3 installed on your computer.

### Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/ipssachin/luncecoscore_AI.git
   cd luncecoscore_AI
   ```

2. Set up a Python Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the application!
   ```bash
   streamlit run app.py
   ```

---

## 🧠 How to Add New AI Models

This app relies on Google's [Teachable Machine](https://teachablemachine.withgoogle.com/) for its AI brains. It is designed to be fully customizable!

To train the app on new items (like adding "Carrots" or "Pizza"):
1. Go to **Teachable Machine** and create an Image Project.
2. Add your classes (e.g., "Carrot", "Sushi").
   > **⚠️ IMPORTANT:** ALWAYS add a class called **`Background`** and take 50+ pictures of your empty room/hands! This prevents the AI from wildly guessing when no food is on screen!
3. Click **Train Model**.
4. Click **Export Model** -> Select **TensorFlow Lite (Floating point)** and download.
5. Create a new folder inside the `models/` directory in this project (e.g., `models/my_new_foods/`).
6. Extract the downloaded `model_unquant.tflite` and `labels.txt` files into that new folder.
7. Open the app, go to the **Admin Dashboard**, and add the environmental stats for your new foods.
8. Go back to the **Scanner Mode**, select your new model from the dropdown, and start scanning!

---

## 🛠️ Technology Stack
- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **Machine Learning Inference**: TensorFlow Lite (`tf-nightly`)
- **Image Processing**: OpenCV (`opencv-python-headless`) & Pillow (PIL)
- **Data Persistence**: Local JSON (`food_data.json`)
