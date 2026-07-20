from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Set font
        self.set_font('helvetica', 'B', 24)
        # Title color (Eco green)
        self.set_text_color(78, 205, 196)
        # Title
        self.cell(0, 15, 'The Eco Lunch Scanner Guide!', align='C')
        self.ln(20)

    def chapter_title(self, title):
        # Set font
        self.set_font('helvetica', 'B', 16)
        # Background color
        self.set_fill_color(255, 107, 107) # Coral pink
        self.set_text_color(255, 255, 255)
        # Title
        self.cell(0, 10, title, fill=True, align='L')
        self.ln(15)

    def chapter_body(self, body):
        # Set font
        self.set_font('helvetica', '', 14)
        self.set_text_color(44, 62, 80)
        # Output text
        self.multi_cell(0, 8, body)
        self.ln(10)

def create_pdf():
    pdf = PDF()
    pdf.add_page()
    
    # Section 1
    pdf.chapter_title('1. What is the Eco Lunch Scanner? ')
    text1 = (
        "Welcome to the Eco Lunch Scanner!\n\n"
        "Have you ever wondered how much water it takes to grow an apple? "
        "Or how much carbon gas is released to make a pizza?\n\n"
        "This fun app uses smart Artificial Intelligence (AI) to look at your food and tell you exactly how it impacts our beautiful planet Earth!"
    )
    pdf.chapter_body(text1)
    
    # Section 2
    pdf.chapter_title('2. How to use the Scanner')
    text2 = (
        "Using the app is as easy as 1, 2, 3:\n\n"
        "Step 1: Open the 'Scanner Mode' in the app.\n"
        "Step 2: Hold your food up to the camera (like an Apple or a Banana).\n"
        "Step 3: Click the 'Take Photo' button.\n\n"
        "The AI will think for a second and then tell you what it sees!"
    )
    pdf.chapter_body(text2)
    
    # Section 3
    pdf.chapter_title('3. What do the scores mean?')
    text3 = (
        "When you scan a food, you get a special scorecard:\n\n"
        "* Water Usage (Drops): This shows how many liters of water were needed to grow or make your food. Less water means a happier planet!\n\n"
        "* Carbon Footprint (Clouds): This is how much invisible gas went into the air during farming and transport. A lower number is better for the climate!\n\n"
        "* Eco Score (0 to 100): This is the final grade! 100 means the food is SUPER good for the Earth. If the score is low, it means that food takes a lot of resources to make."
    )
    pdf.chapter_body(text3)
    
    # Section 4
    pdf.chapter_title('4. Be an Eco-Hero!')
    text4 = (
        "By learning about your food, you are taking the first step to becoming a true Earth Hero! "
        "Try to eat more foods with a High Eco Score (like Apples and Salads) to help save water and protect nature.\n\n"
        "Have fun scanning your lunch!"
    )
    pdf.chapter_body(text4)
    
    pdf.output('Eco_Lunch_Scanner_Kids_Guide.pdf')
    print("PDF generated successfully!")

if __name__ == '__main__':
    create_pdf()
