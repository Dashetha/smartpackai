# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from models.item_schema import ItemInput

client = TestClient(app)

# Test data
TEST_ITEMS = [
    ItemInput(length=10, width=5, height=3, weight=0.5, quantity=1, fragility=0.3),
    ItemInput(length=25, width=18, height=10, weight=1.5, quantity=2, fragility=0.7),
    ItemInput(length=50, width=30, height=20, weight=5.0, quantity=1, fragility=0.9)
]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}

@pytest.mark.parametrize("item", TEST_ITEMS)
def test_predict_box(item: ItemInput):
    response = client.post("/api/predict-box", json=item.dict())
    assert response.status_code == 200
    data = response.json()
    assert "length" in data
    assert "width" in data
    assert "height" in data
    assert data["length"] >= item.length
    assert data["width"] >= item.width
    assert data["height"] >= item.height

def test_optimize_packing():
    test_items = [item.dict() for item in TEST_ITEMS]
    test_box = {"length": 60, "width": 40, "height": 30}
    
    response = client.post(
        "/api/optimize-pack",
        json={"items": test_items, "box": test_box}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == len(TEST_ITEMS)
    assert "space_utilization" in data
    assert 0 < data["space_utilization"] <= 1

def test_invalid_input():
    response = client.post("/api/predict-box", json={"length": -5, "width": 0, "height": 10})
    assert response.status_code == 422