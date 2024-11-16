import requests
import os
from dotenv import load_load_dotenv

load_dotenv()

class FoodAnalyzer:
    def __init__(self):
        # Initialize with your API key
        self.api_key = os.getenv('LOGMEAL_API_KEY')
        self.api_url = "https://api.logmeal.es/v2/recognition/complete"
        
    def analyze_image(self, image_path):
        try:
            # Prepare the image for API request
            with open(image_path, 'rb') as img:
                files = {'image': img}
                headers = {'Authorization': f'Bearer {self.api_key}'}
                
                # Make API request
                response = requests.post(
                    self.api_url,
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return self.format_results(data)
                else:
                    return {'error': 'API request failed'}
                    
        except Exception as e:
            return {'error': str(e)}
    
    def format_results(self, api_response):
        """Format the API response into a clean structure"""
        return {
            'food_items': api_response.get('food_items', []),
            'nutritional_info': {
                'calories': api_response.get('nutritional_info', {}).get('calories'),
                'protein': api_response.get('nutritional_info', {}).get('protein'),
                'carbs': api_response.get('nutritional_info', {}).get('carbs'),
                'fat': api_response.get('nutritional_info', {}).get('fat')
            }
        }