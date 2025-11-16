from fastapi import APIRouter
from app.database import get_database
from app.config import settings
from typing import Dict, List

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    db = get_database()
    
    total_employees = await db.employees.count_documents({})
    promoted = await db.employees.count_documents({"is_promoted": 1})
    promotion_rate = (promoted / total_employees * 100) if total_employees > 0 else 0
    
    # Calculate metrics
    hiring_cost = calculate_hiring_cost(promotion_rate)
    
    # Department stats
    dept_pipeline = [
        {"$group": {
            "_id": "$department",
            "count": {"$sum": 1},
            "promoted": {"$sum": "$is_promoted"}
        }},
        {"$project": {
            "department": "$_id",
            "total": "$count",
            "promoted": 1,
            "promotion_rate": {"$multiply": [{"$divide": ["$promoted", "$count"]}, 100]}
        }}
    ]
    dept_stats = await db.employees.aggregate(dept_pipeline).to_list(length=100)
    
    return {
        "total_employees": total_employees,
        "promoted_count": promoted,
        "promotion_rate": round(promotion_rate, 2),
        "hiring_cost": hiring_cost,
        "by_department": dept_stats
    }

@router.get("/training-score-analysis")
async def training_score_analysis():
    """Analyze training scores vs promotions"""
    db = get_database()
    
    pipeline = [
        {"$group": {
            "_id": "$is_promoted",
            "avg_training_score": {"$avg": "$avg_training_score"},
            "count": {"$sum": 1}
        }}
    ]
    
    results = await db.employees.aggregate(pipeline).to_list(length=10)
    
    return {
        "analysis": results,
        "insight": "Employees promoted have higher avg_training_score (mean: 71) vs not promoted (mean: 62)"
    }

@router.get("/previous-rating-analysis")
async def previous_rating_analysis():
    """Analyze previous year ratings vs promotions"""
    db = get_database()
    
    pipeline = [
        {"$match": {"previous_year_rating": {"$ne": None}}},
        {"$group": {
            "_id": "$is_promoted",
            "avg_rating": {"$avg": "$previous_year_rating"},
            "median_rating": {"$median": {"input": "$previous_year_rating", "method": "approximate"}},
            "count": {"$sum": 1}
        }}
    ]
    
    results = await db.employees.aggregate(pipeline).to_list(length=10)
    
    return {
        "analysis": results,
        "insight": "Employees promoted have higher previous_year_rating (median: 4) vs not promoted (median: 3)"
    }

@router.post("/sensitivity-analysis")
async def sensitivity_analysis(params: Dict):
    """Perform sensitivity analysis"""
    feature = params.get('feature', 'avg_training_score')
    increments = params.get('increments', list(range(-100, 101, 10)))
    
    current_promotion_rate = 8.52  # from dataset
    
    results = []
    for increment in increments:
        # Simplified simulation
        increment_pct = increment / 100.0
        
        if feature == 'avg_training_score':
            # Based on deck: 20% increase = 8.12% promotion rate increase
            promotion_change = increment_pct * 40.6  # approximate relationship
        elif feature == 'previous_year_rating':
            # Based on deck: 10% increase = 1% promotion rate increase
            promotion_change = increment_pct * 10
        else:
            promotion_change = increment_pct * 5
        
        new_rate = current_promotion_rate + promotion_change
        new_rate = max(0, min(100, new_rate))  # clamp between 0-100
        
        results.append({
            "increment": increment_pct,
            "promotion_rate": round(new_rate, 2)
        })
    
    return {
        "feature": feature,
        "current_promotion_rate": current_promotion_rate,
        "analysis": results
    }

@router.post("/business-simulation")
async def business_simulation(params: Dict):
    """Run business simulation"""
    avg_training_improvement = params.get('avg_training_improvement', 0)
    prev_rating_improvement = params.get('prev_rating_improvement', 0)
    
    # Current metrics
    current_promotion_rate = 8.52
    current_hiring_cost = calculate_hiring_cost(current_promotion_rate)
    
    # Calculate new promotion rate
    new_promotion_rate = current_promotion_rate
    
    if avg_training_improvement > 0:
        new_promotion_rate += (avg_training_improvement / 10) * 3.9
    
    if prev_rating_improvement > 0:
        new_promotion_rate += (prev_rating_improvement / 10) * 1.0
    
    new_hiring_cost = calculate_hiring_cost(new_promotion_rate)
    
    promotion_rate_change = new_promotion_rate - current_promotion_rate
    hiring_cost_reduction = ((current_hiring_cost - new_hiring_cost) / current_hiring_cost * 100)
    
    return {
        "before": {
            "promotion_rate": round(current_promotion_rate, 2),
            "hiring_cost": round(current_hiring_cost, 2)
        },
        "after": {
            "promotion_rate": round(new_promotion_rate, 2),
            "hiring_cost": round(new_hiring_cost, 2)
        },
        "improvements": {
            "promotion_rate_increase": round(promotion_rate_change, 2),
            "hiring_cost_reduction_pct": round(hiring_cost_reduction, 2),
            "cost_saved": round(current_hiring_cost - new_hiring_cost, 2)
        }
    }

@router.get("/recommendations")
async def get_recommendations():
    """Get improvement recommendations"""
    return {
        "training_recommendations": [
            {
                "problem": "Poor training system",
                "recommendation": "Build and subscribe corporate LMS",
                "pros": ["Easy to track progress", "Unlimited learning access"],
                "cons": ["Cost investment required"]
            },
            {
                "problem": "Hard to get access",
                "recommendation": "Mobile-friendly LMS with user-friendly interface",
                "pros": ["Access anytime anywhere", "Higher completion rates"],
                "cons": ["Development time and cost"]
            },
            {
                "problem": "Lack of leadership training",
                "recommendation": "Create leadership and soft skill courses",
                "pros": ["Improved performance", "Higher productivity"],
                "cons": ["Time to build courses"]
            }
        ],
        "rating_recommendations": [
            {
                "problem": "No transparency in ratings",
                "recommendation": "Improve feedback process with constructive feedback",
                "pros": ["Employees understand strengths/weaknesses"],
                "cons": ["100% transparency can cause issues"]
            },
            {
                "problem": "Subjective performance reviews",
                "recommendation": "Create objective performance review system",
                "pros": ["Fair objective assessment"],
                "cons": ["Hard to be 100% objective for all roles"]
            }
        ]
    }

def calculate_hiring_cost(promotion_rate: float) -> float:
    """Calculate hiring cost based on promotion rate"""
    avg_cost_per_hire = settings.AVG_COST_PER_HIRING
    hiring_target_pct = settings.HIRING_TARGET_PERCENTAGE
    total_employees = settings.TOTAL_NUM_EMPLOYEES
    
    num_recruited = hiring_target_pct * (1 - promotion_rate/100) * total_employees
    total_cost = num_recruited * avg_cost_per_hire
    
    return total_cost / 1000000  # in millions
