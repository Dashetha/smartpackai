# tests/test_packing.py
import pytest
from services.pack_optimizer import PackingOptimizer
from models.item_schema import ItemInput, BoxOutput

# Test data
TEST_ITEMS = [
    ItemInput(length=10, width=10, height=10, weight=1.0),
    ItemInput(length=5, width=5, height=20, weight=0.5),
    ItemInput(length=15, width=15, height=5, weight=1.5)
]

TEST_BOX = BoxOutput(length=30, width=30, height=30)

def test_packing_optimization():
    optimizer = PackingOptimizer()
    result = optimizer.optimize(TEST_ITEMS, TEST_BOX)
    
    assert len(result.items) == len(TEST_ITEMS)
    assert 0 < result.space_utilization <= 1
    assert len(result.packing_instructions) > 0
    
    # Verify all items are within box dimensions
    for packed_item in result.items:
        assert 0 <= packed_item.position.x <= TEST_BOX.length - packed_item.item.length
        assert 0 <= packed_item.position.y <= TEST_BOX.width - packed_item.item.width
        assert 0 <= packed_item.position.z <= TEST_BOX.height - packed_item.item.height

def test_fragile_item_handling():
    fragile_item = ItemInput(length=10, width=10, height=10, weight=1.0, fragility=0.9)
    optimizer = PackingOptimizer()
    result = optimizer.optimize([fragile_item], TEST_BOX)
    
    assert "Extra padding" in result.packing_instructions[1]
    assert "foam" in result.recommended_void_fill.lower()

@pytest.mark.parametrize("quantity", [1, 3, 5])
def test_multiple_quantities(quantity: int):
    item = ItemInput(length=5, width=5, height=5, weight=0.1, quantity=quantity)
    optimizer = PackingOptimizer()
    result = optimizer.optimize([item], TEST_BOX)
    
    assert len(result.items) == quantity