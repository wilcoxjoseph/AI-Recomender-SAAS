from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String, index=True)
    embedding = Column(Text)  # Store as JSON string or use pgvector

class UserInteraction(Base):
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    rating = Column(Integer)  # 1-5 or null for implicit
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SavedRecommendation(Base):
    __tablename__ = "saved_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    saved_at = Column(DateTime(timezone=True), server_default=func.now())
