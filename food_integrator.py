from ultralytics import YOLO
import cv2
import numpy as np

class FoodDetector:
    def __init__(self):
        # Initialize YOLO model
        self.model = YOLO('static/models/yolov8s.pt')
        
    def analyze_image(self, image):
        # Detect food items in image
        results = self.model(image)
        detections = []
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                confidence = box.conf[0]
                class_id = box.cls[0]
                
                # Only include food-related classes
                if self.model.names[int(class_id)] in self.get_food_classes():
                    detections.append({
                        'food_item': self.model.names[int(class_id)],
                        'confidence': float(confidence),
                        'bbox': [float(x1), float(y1), float(x2), float(y2)]
                    })
        
        return detections
    
    def estimate_portion_size(self, bbox, depth_map):
        x1, y1, x2, y2 = bbox
        region = depth_map[int(y1):int(y2), int(x1):int(x2)]
        # Implement volume calculation logic here
        return self.calculate_volume(region)
    
    @staticmethod
    def get_food_classes():
        # Return list of food-related class names
        return ['apple', 'banana', 'orange', 'pizza', 'sandwich', 'carrot']
    
    @staticmethod
    def calculate_volume(region):
        # Implement volume calculation logic
        return np.mean(region) * region.shape[0] * region.shape[1]