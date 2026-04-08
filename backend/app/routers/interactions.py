from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..auth import verify_token
from .. import models

router = APIRouter(prefix="/api/interactions", tags=["interactions"])

class InteractionCreate(BaseModel):
    item_id: int
    rating: int  # 1-5

@router.post("/")
async def create_interaction(
    interaction: InteractionCreate,
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Record user rating/like for an item"""
    
    # Check if item exists
    item = db.query(models.Item).filter(models.Item.id == interaction.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Create interaction
    db_interaction = models.UserInteraction(
        user_id=current_user.id,
        item_id=interaction.item_id,
        rating=interaction.rating
    )
    db.add(db_interaction)
    db.commit()
    
    return {"message": "Interaction recorded successfully"}

@router.get("/user")
async def get_user_interactions(
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get all interactions for current user"""
    interactions = db.query(models.UserInteraction).filter(
        models.UserInteraction.user_id == current_user.id
    ).all()
    
    return {
        "interactions": [
            {
                "item_id": i.item_id,
                "rating": i.rating,
                "created_at": i.created_at
            }
            for i in interactions
        ]
    }
