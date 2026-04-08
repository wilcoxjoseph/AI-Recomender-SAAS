from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import verify_token
from ..recommender import RecommenderSystem

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

# Initialize recommender globally
recommender = RecommenderSystem()

@router.get("/")
async def get_recommendations(
    current_user=Depends(verify_token),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get personalized recommendations for current user"""
    # Initialize recommender if not already done
    if recommender.index is None:
        recommender.initialize_from_db(db)
    
    recommendations = recommender.recommend(db, current_user.id, limit)
    
    return {
        "user_id": str(current_user.id),
        "recommendations": [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "category": item.category
            }
            for item in recommendations
        ]
    }
