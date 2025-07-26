# ml_model/predict.py
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class BoxSizePredictor:
    def __init__(self, model_path: str = None):
        self.model = self._load_model(model_path)
        self.standard_boxes = [
            (20, 15, 10), (25, 20, 15), (30, 25, 20),
            (40, 30, 20), (50, 40, 30)
        ]
        
    def _load_model(self, model_path: str):
        """Load trained model from file"""
        try:
            if model_path is None:
                model_path = Path(__file__).parent / 'model.pkl'
            return joblib.load(model_path)
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise

    def _select_nearest_standard(self, pred_length: float, pred_width: float, pred_height: float) -> Dict:
        """Find closest standard box size"""
        best_match = None
        min_diff = float('inf')
        
        for box in self.standard_boxes:
            # Calculate volume difference
            std_volume = box[0] * box[1] * box[2]
            pred_volume = pred_length * pred_width * pred_height
            volume_diff = abs(std_volume - pred_volume)
            
            # Check dimensional constraints
            length_ok = box[0] >= pred_length
            width_ok = box[1] >= pred_width
            height_ok = box[2] >= pred_height
            
            if length_ok and width_ok and height_ok and volume_diff < min_diff:
                min_diff = volume_diff
                best_match = {
                    'length': box[0],
                    'width': box[1],
                    'height': box[2],
                    'volume': std_volume,
                    'is_custom': False
                }
        
        return best_match or {
            'length': round(pred_length + 2, 1),  # Add 2cm padding
            'width': round(pred_width + 2, 1),
            'height': round(pred_height + 2, 1),
            'volume': round((pred_length + 2) * (pred_width + 2) * (pred_height + 2), 1),
            'is_custom': True
        }

    def predict(self, item_length: float, item_width: float, item_height: float,
                item_weight: float, quantity: int = 1, fragility: float = 0.5) -> Dict:
        """Predict optimal box dimensions"""
        try:
            # Prepare input features
            input_data = pd.DataFrame([[
                item_length, item_width, item_height,
                item_weight, quantity, fragility
            ]], columns=[
                'item_length', 'item_width', 'item_height',
                'item_weight', 'quantity', 'fragility'
            ])
            
            # Make prediction
            pred = self.model.predict(input_data)[0]
            pred_length, pred_width, pred_height = pred
            
            # Select standard box or create custom
            box = self._select_nearest_standard(pred_length, pred_width, pred_height)
            
            return {
                'status': 'success',
                'predicted_dimensions': {
                    'length': round(pred_length, 2),
                    'width': round(pred_width, 2),
                    'height': round(pred_height, 2)
                },
                'recommended_box': box,
                'metrics': {
                    'space_efficiency': round(
                        (item_length * item_width * item_height * quantity) / box['volume'], 3
                    )
                }
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

# Singleton predictor instance
predictor = BoxSizePredictor()

def predict_box_dimensions(item_length: float, item_width: float, item_height: float,
                          item_weight: float, quantity: int = 1, fragility: float = 0.5):
    """Public prediction interface"""
    return predictor.predict(item_length, item_width, item_height,
                           item_weight, quantity, fragility)