import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import base64

app = Flask(__name__)
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def create_system_message():
    return """You are a nutrition expert specialized in analyzing food images. When given an image, please:
1. Identify all food items in the image
2. Estimate calories for each item
3. Provide nutritional information including protein, carbs, and fats
4. Format the response in a clean JSON structure
5. Keep descriptions concise and focused on nutritional content"""

def analyze_food_image(image_base64):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": create_system_message()
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_base64
                            }
                        },
                        {
                            "type": "text",
                            "text": "Analyze this food image and provide nutritional information including calories, protein, carbs, and fats. Format the response as JSON."
                        }
                    ]
                }
            ],
            model="llava-v1.5-7b-groq",
            max_tokens=1024,
            temperature=0.1,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Convert image to base64
    image_data = file.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    
    # Analyze image using Groq
    analysis_result = analyze_food_image(image_base64)
    
    return jsonify({
        'analysis': analysis_result
    })

if __name__ == '__main__':
    app.run(debug=True)