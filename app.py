from flask import Flask, request, jsonify
import cv2
import numpy as np
from food_detector import FoodDetector
from nutrition_database import NutritionDB
#HI vir its troy
#its me mario
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
def analyze_food():
    try:
        # Get image from request
        image = request.files['image'].read()
        nparr = np.fromstring(image, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Detect food items
        detected_items = food_detector.analyze_image(img)
        
        # Get nutritional information
        nutritional_info = nutrition_db.get_nutrition_data(detected_items)
        
        return jsonify({
            'status': 'success',
            'detected_items': detected_items,
            'nutritional_info': nutritional_info
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)