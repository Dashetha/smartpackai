# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.item_schema import ItemInput, BoxOutput, PackingPlan
from services.box_predictor import predict_box_size
from services.pack_optimizer import optimize_packing
from typing import List
import logging

app = FastAPI(
    title="SmartPack AI API",
    description="Optimal Packaging Recommendation System",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.post("/api/predict-box", response_model=BoxOutput)
async def predict_box(item: ItemInput):
    """
    Predict optimal box size for given item dimensions
    """
    try:
        logger.info(f"Received box prediction request for item: {item}")
        box = predict_box_size(item)
        return box
    except Exception as e:
        logger.error(f"Box prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/optimize-pack", response_model=PackingPlan)
async def optimize_pack(items: List[ItemInput], box: BoxOutput):
    """
    Optimize packing arrangement for items in given box
    """
    try:
        logger.info(f"Received packing optimization request for {len(items)} items")
        plan = optimize_packing(items, box)
        return plan
    except Exception as e:
        logger.error(f"Packing optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Service health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}