import sqlite3
import json

class NutritionDB:
    def __init__(self):
        self.db_path = 'nutrition.db'
        self.setup_database()
        
    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS nutrition_data
                     (food_item TEXT PRIMARY KEY, 
                      calories REAL,
                      protein REAL,
                      carbs REAL,
                      fat REAL)''')
        conn.commit()
        conn.close()
    
    def get_nutrition_data(self, detected_items):
        conn = sqlite3.connect(self.db_path)
        nutrition_info = {}
        
        for item in detected_items:
            food = item['food_item']
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM nutrition_data WHERE food_item = ?', 
                         (food,))
            result = cursor.fetchone()
            
            if result:
                nutrition_info[food] = {
                    'calories': result[1],
                    'protein': result[2],
                    'carbs': result[3],
                    'fat': result[4]
                }
            else:
                # If not in database, fetch from external API
                nutrition_info[food] = self.fetch_from_api(food)
        
        conn.close()
        return nutrition_info
    
    def fetch_from_api(self, food_item):
        # Implement API call to nutrition database
        # This is a placeholder implementation
        default_values = {
            'calories': 100,
            'protein': 2,
            'carbs': 15,
            'fat': 1
        }
        return default_values