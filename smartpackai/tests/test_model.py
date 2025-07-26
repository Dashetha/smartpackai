# tests/test_model.py
import pytest
import joblib
import numpy as np
from ml_model.predict import BoxSizePredictor
from models.item_schema import ItemInput

# Sample test data
TEST_ITEMS = [
    ItemInput(length=10, width=5, height=3, weight=0.5),
    ItemInput(length=25, width=18, height=10, weight=1.5),
    ItemInput(length=50, width=30, height=20, weight=5.0)
]

def test_model_loading():
    predictor = BoxSizePredictor()
    assert hasattr(predictor.model, "predict")
    
    # Test prediction shape
    sample_input = np.array([[10, 5, 3, 0.5, 1, 0.5]])
    prediction = predictor.model.predict(sample_input)
    assert prediction.shape == (1, 3)

@pytest.mark.parametrize("item", TEST_ITEMS)
def test_prediction(item: ItemInput):
    predictor = BoxSizePredictor()
    result = predictor.predict(
        item.length, item.width, item.height,
        item.weight, item.quantity, item.fragility
    )
    
    assert result["status"] == "success"
    assert result["predicted_dimensions"]["length"] >= item.length
    assert result["predicted_dimensions"]["width"] >= item.width
    assert result["predicted_dimensions"]["height"] >= item.height
    assert result["metrics"]["space_efficiency"] > 0

def test_standard_box_selection():
    predictor = BoxSizePredictor()
    # Test case that should match standard box (30x25x20)
    result = predictor.predict(25, 18, 10, 1.5)
    assert not result["recommended_box"]["is_custom"]
    assert result["recommended_box"]["length"] == 30
    assert result["recommended_box"]["width"] == 25
    assert result["recommended_box"]["height"] == 20