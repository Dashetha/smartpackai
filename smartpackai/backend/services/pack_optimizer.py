# backend/services/pack_optimizer.py
from typing import List, Dict
import numpy as np
from models.item_schema import ItemInput, BoxOutput, PackingPlan, PackedItem, Position, Rotation
import logging

logger = logging.getLogger(__name__)

class PackingOptimizer:
    def __init__(self):
        self.padding_thickness = {
            "bubble_wrap": 2.0,
            "air_cushions": 3.0,
            "foam_peanuts": 5.0
        }

    def _calculate_padding(self, fragility: float, void_fill: str) -> float:
        """Calculate required padding thickness"""
        base_thickness = self.padding_thickness.get(void_fill, 2.0)
        return base_thickness * (1 + fragility)

    def optimize(self, items: List[ItemInput], box: BoxOutput) -> PackingPlan:
        """Optimize packing arrangement (simplified implementation)"""
        try:
            # Sort items by volume (largest first)
            sorted_items = sorted(
                items,
                key=lambda x: x.length * x.width * x.height * x.quantity,
                reverse=True
            )

            packed_items = []
            z_position = 0
            
            for item in sorted_items:
                # Simple packing logic - place items vertically stacked
                for _ in range(item.quantity):
                    packed_items.append(
                        PackedItem(
                            item=item,
                            position=Position(
                                x=0,
                                y=0,
                                z=z_position
                            ),
                            rotation=Rotation()
                        )
                    )
                    z_position += item.height + self._calculate_padding(
                        item.fragility,
                        box.recommended_void_fill
                    )

            # Calculate space utilization
            total_item_volume = sum(
                i.length * i.width * i.height * i.quantity
                for i in items
            )
            utilization = total_item_volume / box.volume

            # Generate packing instructions
            instructions = [
                "Place heaviest items at the bottom",
                f"Use {box.recommended_void_fill.replace('_', ' ')} for padding",
                "Fill empty spaces with cushioning material",
                "Seal box with reinforced tape"
            ]

            if any(i.fragility > 0.7 for i in items):
                instructions.insert(1, "Extra padding for fragile items")

            return PackingPlan(
                box=box,
                items=packed_items,
                space_utilization=utilization,
                estimated_cost_saving=self._estimate_cost_saving(utilization),
                packing_instructions=instructions
            )

        except Exception as e:
            logger.error(f"Packing optimization failed: {str(e)}")
            raise

    def _estimate_cost_saving(self, utilization: float) -> float:
        """Estimate cost savings based on space utilization"""
        # Simple heuristic - better utilization = higher savings
        base_saving = 5.0  # USD
        return base_saving * utilization

# Singleton optimizer instance
optimizer = PackingOptimizer()

def optimize_packing(items: List[ItemInput], box: BoxOutput) -> PackingPlan:
    """Public interface for packing optimization"""
    return optimizer.optimize(items, box)