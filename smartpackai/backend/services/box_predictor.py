# backend/services/box_predictor.py
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from models.item_schema import ItemInput, BoxOutput
from typing import Dict
import logging

logger = logging.getLogger(__name__)

# Mock model - replace with actual trained model
class BoxPredictor:
    def __init__(self):
        self.model = self._load_model()
        self.standard_boxes = [
            (20, 15, 10), (25, 20, 15), (30, 25, 20),
            (40, 30, 20), (50, 40, 30)
        ]
        self.void_fill_materials = {
            "low": "bubble_wrap",
            "medium": "air_cushions",
            "high": "foam_peanuts"
        }

    def _load_model(self):
        """Load pre-trained model (mock implementation)"""
        # In production, load actual trained model
        return RandomForestRegressor(n_estimators=10)  # Dummy model

    def _predict_volume(self, item: ItemInput) -> float:
        """Predict required box volume (mock implementation)"""
        # Base volume calculation with fragility factor
        base_volume = item.length * item.width * item.height * item.quantity
        fragility_factor = 1 + (item.fragility * 0.3)  # 0-30% extra space
        return base_volume * fragility_factor

    def _select_standard_box(self, predicted_volume: float) -> Dict:
        """Select closest standard box"""
        best_box = None
        best_volume_diff = float('inf')
        
        for box in self.standard_boxes:
            box_volume = box[0] * box[1] * box[2]
            volume_diff = box_volume - predicted_volume
            
            if volume_diff >= 0 and volume_diff < best_volume_diff:
                best_volume_diff = volume_diff
                best_box = {
                    "length": box[0],
                    "width": box[1],
                    "height": box[2],
                    "volume": box_volume
                }
        
        return best_box or {
            "length": round(np.sqrt(predicted_volume) * 1.2),
            "width": round(np.sqrt(predicted_volume) * 0.8),
            "height": round(np.sqrt(predicted_volume) * 0.6),
            "volume": predicted_volume
        }

    def predict(self, item: ItemInput) -> BoxOutput:
        """Main prediction method"""
        try:
            predicted_volume = self._predict_volume(item)
            box = self._select_standard_box(predicted_volume)
            
            # Determine void fill material based on fragility
            if item.fragility < 0.3:
                void_fill = self.void_fill_materials["low"]
            elif item.fragility < 0.7:
                void_fill = self.void_fill_materials["medium"]
            else:
                void_fill = self.void_fill_materials["high"]
            
            return BoxOutput(
                length=box["length"],
                width=box["width"],
                height=box["height"],
                volume=box["volume"],
                recommended_void_fill=void_fill
            )
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise

# Singleton predictor instance
predictor = BoxPredictor()

def predict_box_size(item: ItemInput) -> BoxOutput:
    """Public interface for box prediction"""
    return predictor.predict(item)