from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import verify_token
from .. import models

router = APIRouter(prefix="/api/saved", tags=["saved"])

@router.post("/{item_id}")
async def save_item(
    item_id: int,
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Save an item to user's saved list"""
    
    # Check if already saved
    existing = db.query(models.SavedRecommendation).filter(
        models.SavedRecommendation.user_id == current_user.id,
        models.SavedRecommendation.item_id == item_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Item already saved")
    
    saved = models.SavedRecommendation(
        user_id=current_user.id,
        item_id=item_id
    )
    db.add(saved)
    db.commit()
    
    return {"message": "Item saved successfully"}

@router.delete("/{item_id}")
async def unsave_item(
    item_id: int,
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Remove item from saved list"""
    
    saved = db.query(models.SavedRecommendation).filter(
        models.SavedRecommendation.user_id == current_user.id,
        models.SavedRecommendation.item_id == item_id
    ).first()
    
    if not saved:
        raise HTTPException(status_code=404, detail="Saved item not found")
    
    db.delete(saved)
    db.commit()
    
    return {"message": "Item removed from saved"}

@router.get("/")
async def get_saved_items(
    current_user=Depends(verify_token),
    db: Session = Depends(get_db)
):
    """Get all saved items for current user"""
    
    saved = db.query(models.SavedRecommendation).filter(
        models.SavedRecommendation.user_id == current_user.id
    ).all()
    
    items = []
    for s in saved:
        item = db.query(models.Item).filter(models.Item.id == s.item_id).first()
        if item:
            items.append({
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "category": item.category,
                "saved_at": s.saved_at
            })
    
    return {"saved_items": items}
