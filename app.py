from flask import Flask, request, jsonify
import cv2
import numpy as np
from food_detector import FoodDetector
from nutrition_database import NutritionDB

app = Flask(__name__)
food_detector = FoodDetector()
nutrition_db = NutritionDB()

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