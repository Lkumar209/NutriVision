import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import time

# Load environment variables
load_dotenv()

# Configure the API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set page configuration
st.set_page_config(
    page_title="NutriVision",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme with additional fixes for file uploader
st.markdown("""
<style>
    /* Overall page background */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    
    /* Remove all default white containers and backgrounds */
    div.block-container {
        padding-top: 2rem;
    }
    
    div.stFileUploader, section, div.stAlert, div[data-testid="stForm"] {
        background-color: #1e1e1e !important;
        border-color: #333333 !important;
    }
    
    /* Target ALL white boxes and containers */
    div, section, header, footer, main, article, aside, nav, form, label, input, button {
        background-color: transparent !important;
        color: #e0e0e0 !important;
    }
    
    /* Specific white box fix - targeting all possible elements with background */
    [class*="css"], [class*="st-"], [data-testid*="st"], .stMarkdown {
        background-color: transparent !important;
    }
    
    /* Special fix for file uploader */
    .stFileUploader > div, .stFileUploader > div > div, [data-testid="stFileUploader"] {
        background-color: #1e1e1e !important;
        color: #e0e0e0 !important;
        border-radius: 10px !important;
    }
    
    /* The file uploader drop area */
    .stFileUploader > div > div > div, [data-testid="stFileUploadDropzone"] {
        background-color: #2d3748 !important;
        border: 1px dashed #4a5568 !important;
        color: #e0e0e0 !important;
    }
    
    /* Main container styling */
    .main-container {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    
    /* Custom card container */
    .card-container {
        background-color: #2d3748 !important;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }
    
    .logo-text {
        color: #4CAF50;
        font-size: 2.5rem;
        font-weight: 700;
        margin-left: 0.5rem;
    }
    
    /* Streamlit button customization */
    .stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: 500;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #3e8e41 !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }
    
    /* Header styling */
    h1 {
        color: #6FCF97 !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Subheader styling */
    h2, h3 {
        color: #BBBBBB !important;
        font-weight: 500 !important;
        margin-bottom: 1rem !important;
    }
    
    /* Results container */
    .results-container {
        background-color: #2d3748 !important;
        border-radius: 8px;
        padding: 1.5rem;
        margin-top: 2rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: #888;
        margin-top: 3rem;
        font-size: 0.8rem;
        padding: 1rem;
        border-top: 1px solid #333;
    }
    
    /* Markdown text */
    p, li, span {
        color: #BBBBBB !important;
    }
    
    /* Spinner */
    .stSpinner > div > div {
        border-color: #4CAF50 transparent transparent !important;
    }
    
    /* Caption text */
    .caption {
        color: #999999 !important;
    }
    
    /* Upload icon styling */
    .upload-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
        color: #4CAF50;
    }
    
    /* Browse files button */
    button[data-testid="stFileUploaderDropzoneButtonText"] {
        background-color: #333 !important;
        color: #CCC !important;
        border-radius: 5px !important;
        border: 1px solid #555 !important;
        transition: all 0.3s ease;
    }
    
    button[data-testid="stFileUploaderDropzoneButtonText"]:hover {
        background-color: #444 !important;
        border-color: #666 !important;
    }
</style>
""", unsafe_allow_html=True)

def get_gemini_response(input_prompt, image):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_prompt, image[0]])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Custom logo and header
st.markdown("""
<div class="logo-container">
    <img src="https://img.icons8.com/color/48/000000/salad.png" alt="Salad Icon" width="48" height="48">
    <span class="logo-text">NutriVision</span>
</div>
""", unsafe_allow_html=True)

# Subtitle
st.markdown("<h3 style='text-align: center; font-weight: 400; color: #888;'>AI-Powered Nutrition Analysis</h3>", unsafe_allow_html=True)

# Card container for main content
st.markdown("<div class='card-container'>", unsafe_allow_html=True)

# App description
st.markdown("""
Take a photo of your meal and instantly get nutritional information, calorie count, 
and personalized health recommendations.
""")

# Custom file upload label
st.markdown("""
<div style="margin: 1.5rem 0 1rem 0;">
    <span class="upload-icon">📸</span>
    <span style="font-size: 1.1rem; font-weight: 500;">Upload Food Image</span>
</div>
""", unsafe_allow_html=True)

# File upload section
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

# Image preview and analysis
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Create a nice card for the uploaded image
    st.markdown("<div class='card-container' style='background-color: #253245 !important;'>", unsafe_allow_html=True)
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(image, caption="", use_column_width=True)
    
    with col2:
        st.markdown("<h3 style='color: #6FCF97 !important;'>Ready for Analysis</h3>", unsafe_allow_html=True)
        st.markdown("Your food image has been successfully uploaded. Click below to analyze its nutritional content.")
        
        # Submit button with better styling
        st.markdown("<div style='margin-top: 1.5rem;'>", unsafe_allow_html=True)
        submit = st.button("Analyze Nutrition 🔍")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Input prompt with detailed instructions
input_prompt = """
You are NutriVision, an advanced AI nutritionist specialized in analyzing food images. Examine the provided image and:

1. Identify all food items visible in the image
2. Calculate the approximate calories for each item
3. Provide nutritional breakdown in this format:

**Food Items and Calories:**
- Item 1: ~XX calories (key nutrients)
- Item 2: ~XX calories (key nutrients)
...

**Total Meal Analysis:**
- Total Calories: XXX
- Protein: XX g
- Carbs: XX g
- Fat: XX g

**Health Assessment:**
[Provide a brief assessment of whether this meal is healthy, balanced, or needs improvement]

**Recommendations:**
[Suggest 2-3 specific, actionable improvements or complementary foods to balance the meal]
"""

# Process the image when submit is clicked
if 'submit' in locals() and submit:
    try:
        st.markdown("<div class='results-container'>", unsafe_allow_html=True)
        
        # Create a loading animation
        with st.spinner("🔍 Analyzing your meal..."):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)
            time.sleep(1)  # Simulate processing time for better UX
        
        # Display results with better formatting
        st.markdown("<h2 style='color: #6FCF97 !important;'>📊 Nutrition Analysis Results</h2>", unsafe_allow_html=True)
        
        # Format the response with custom styling
        formatted_response = response.replace('**', '<span style="color:#6FCF97; font-weight:600;">')
        formatted_response = formatted_response.replace('**', '</span>')
        st.markdown(f"<div style='line-height:1.6;'>{formatted_response}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

st.markdown("</div>", unsafe_allow_html=True)

# Custom footer with better styling
st.markdown("""
<div class='footer'>
    <div style="display: flex; justify-content: center; align-items: center; gap: 1rem;">
        <span>NutriVision</span>
        <span>•</span>
        <span>Powered by Gemini AI</span>
        <span>•</span>
        <span>Created with Streamlit</span>
    </div>
</div>
""", unsafe_allow_html=True)
