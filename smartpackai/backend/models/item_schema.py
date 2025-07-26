# backend/models/item_schema.py
from pydantic import BaseModel, Field
from typing import List, Optional

class ItemInput(BaseModel):
    """Input schema for item dimensions"""
    length: float = Field(..., gt=0, description="Item length in cm")
    width: float = Field(..., gt=0, description="Item width in cm")
    height: float = Field(..., gt=0, description="Item height in cm")
    weight: float = Field(..., gt=0, description="Item weight in kg")
    quantity: int = Field(1, gt=0, description="Number of identical items")
    fragility: float = Field(0.5, ge=0, le=1, description="Fragility rating (0-1)")
    is_rotatable: bool = Field(True, description="Can item be rotated for packing?")

class BoxOutput(BaseModel):
    """Output schema for recommended box"""
    length: float = Field(..., description="Box length in cm")
    width: float = Field(..., description="Box width in cm")
    height: float = Field(..., description="Box height in cm")
    volume: float = Field(..., description="Total volume in cm³")
    recommended_void_fill: str = Field(..., description="Suggested padding material")

class Position(BaseModel):
    """3D position coordinates"""
    x: float
    y: float
    z: float

class Rotation(BaseModel):
    """3D rotation angles"""
    x: float = 0
    y: float = 0
    z: float = 0

class PackedItem(BaseModel):
    """Schema for packed item position"""
    item: ItemInput
    position: Position
    rotation: Rotation

class PackingPlan(BaseModel):
    """Complete packing plan output"""
    box: BoxOutput
    items: List[PackedItem]
    space_utilization: float = Field(..., ge=0, le=1, description="0-1 percentage of space used")
    estimated_cost_saving: float = Field(..., ge=0, description="Estimated shipping cost saving in USD")
    packing_instructions: List[str] = Field(..., description="Step-by-step packing guide")