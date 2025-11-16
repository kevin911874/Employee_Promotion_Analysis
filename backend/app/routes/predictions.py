from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.database import get_database
from datetime import datetime
import pandas as pd
import numpy as np

router = APIRouter()

@router.post("/predict")
async def predict_promotion(employee_data: dict):
    """Predict promotion for a single employee"""
    try:
        # Simple prediction logic based on analysis from the deck
        avg_score = employee_data.get('avg_training_score', 0)
        prev_rating = employee_data.get('previous_year_rating', 0)
        awards = employee_data.get('awards_won', 0)
        
        # Scoring logic
        score = 0
        if avg_score > 70:
            score += 0.4
        elif avg_score > 60:
            score += 0.2
        
        if prev_rating >= 4:
            score += 0.3
        elif prev_rating >= 3:
            score += 0.15
        
        if awards == 1:
            score += 0.2
        
        # Length of service bonus
        if employee_data.get('length_of_service', 0) >= 5:
            score += 0.1
        
        predicted_promotion = 1 if score >= 0.5 else 0
        
        # Save prediction
        db = get_database()
        prediction_record = {
            "employee_id": employee_data.get('employee_id'),
            "predicted_promotion": predicted_promotion,
            "promotion_probability": min(score, 1.0),
            "prediction_date": datetime.utcnow(),
            "input_data": employee_data
        }
        
        await db.predictions.insert_one(prediction_record)
        
        return {
            "employee_id": employee_data.get('employee_id'),
            "predicted_promotion": predicted_promotion,
            "promotion_probability": round(min(score, 1.0), 3),
            "confidence": "High" if abs(score - 0.5) > 0.3 else "Medium"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict-batch")
async def predict_batch(employees_data: List[dict]):
    """Predict promotions for multiple employees"""
    results = []
    for emp_data in employees_data:
        try:
            result = await predict_promotion(emp_data)
            results.append(result)
        except Exception as e:
            results.append({
                "employee_id": emp_data.get('employee_id'),
                "error": str(e)
            })
    return results

@router.get("/history/{employee_id}")
async def get_prediction_history(employee_id: int):
    """Get prediction history for an employee"""
    db = get_database()
    
    cursor = db.predictions.find(
        {"employee_id": employee_id}
    ).sort("prediction_date", -1).limit(10)
    
    predictions = await cursor.to_list(length=10)
    
    for pred in predictions:
        pred["_id"] = str(pred["_id"])
    
    return predictions

@router.get("/recent")
async def get_recent_predictions(limit: int = 50):
    """Get recent predictions"""
    db = get_database()
    
    cursor = db.predictions.find().sort("prediction_date", -1).limit(limit)
    predictions = await cursor.to_list(length=limit)
    
    for pred in predictions:
        pred["_id"] = str(pred["_id"])
    
    return predictions
