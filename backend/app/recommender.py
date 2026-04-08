import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from . import models
import json

class RecommenderSystem:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.item_ids = []
        self.item_embeddings = []
        
    def initialize_from_db(self, db: Session):
        """Load all items from DB and build FAISS index"""
        items = db.query(models.Item).all()
        
        if not items:
            # Load sample data if no items exist
            self._load_sample_data(db)
            items = db.query(models.Item).all()
        
        self.item_ids = []
        embeddings_list = []
        
        for item in items:
            if item.embedding:
                emb = np.array(json.loads(item.embedding), dtype=np.float32)
            else:
                # Generate embedding on the fly
                emb = self.model.encode(item.title + " " + item.description)
                item.embedding = json.dumps(emb.tolist())
                db.commit()
            
            embeddings_list.append(emb)
            self.item_ids.append(item.id)
        
        self.item_embeddings = np.array(embeddings_list)
        
        # Build FAISS index
        dimension = self.item_embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for similarity
        faiss.normalize_L2(self.item_embeddings)
        self.index.add(self.item_embeddings)
    
    def _load_sample_data(self, db: Session):
        """Load sample movie dataset"""
        sample_items = [
            {"title": "Inception", "description": "A thief who steals corporate secrets through dream-sharing technology", "category": "Sci-Fi"},
            {"title": "The Matrix", "description": "A computer hacker learns about the true nature of reality", "category": "Sci-Fi"},
            {"title": "The Godfather", "description": "The aging patriarch of an organized crime dynasty transfers control to his son", "category": "Drama"},
            {"title": "Pulp Fiction", "description": "The lives of two mob hitmen, a boxer, and a pair of diner bandits intertwine", "category": "Crime"},
            {"title": "The Dark Knight", "description": "Batman faces the Joker, a criminal mastermind", "category": "Action"},
            {"title": "Forrest Gump", "description": "The presidencies of Kennedy and Johnson through the eyes of a man with low IQ", "category": "Drama"},
            {"title": "Goodfellas", "description": "The story of Henry Hill and his life in the mob", "category": "Crime"},
            {"title": "The Social Network", "description": "The founding of Facebook", "category": "Drama"},
            {"title": "Interstellar", "description": "A team of explorers travel through a wormhole in space", "category": "Sci-Fi"},
            {"title": "The Wolf of Wall Street", "description": "A stockbroker's rise and fall on Wall Street", "category": "Comedy"},
        ]
        
        for item_data in sample_items:
            item = models.Item(**item_data)
            db.add(item)
        db.commit()
    
    def get_user_embedding(self, db: Session, user_id):
        """Create user embedding based on their rated items"""
        interactions = db.query(models.UserInteraction).filter(
            models.UserInteraction.user_id == user_id,
            models.UserInteraction.rating >= 4  # Only highly-rated items
        ).all()
        
        if not interactions:
            # Cold start - return None for popularity-based recommendations
            return None
        
        # Get embeddings for items user liked
        liked_embeddings = []
        for interaction in interactions:
            item = db.query(models.Item).filter(models.Item.id == interaction.item_id).first()
            if item and item.embedding:
                emb = np.array(json.loads(item.embedding), dtype=np.float32)
                liked_embeddings.append(emb)
        
        if not liked_embeddings:
            return None
        
        # Average embeddings
        user_emb = np.mean(liked_embeddings, axis=0)
        user_emb = user_emb / np.linalg.norm(user_emb)
        return user_emb.reshape(1, -1)
    
    def recommend(self, db: Session, user_id, top_k=10):
        """Get recommendations for user"""
        user_emb = self.get_user_embedding(db, user_id)
        
        if user_emb is None:
            # Cold start - return popular items (most interacted with)
            popular_items = db.query(models.Item.id).join(
                models.UserInteraction
            ).group_by(
                models.Item.id
            ).order_by(
                models.UserInteraction.rating.count().desc()
            ).limit(top_k).all()
            
            item_ids = [item[0] for item in popular_items]
            items = db.query(models.Item).filter(models.Item.id.in_(item_ids)).all()
            
            # If no interactions yet, return random sample
            if not items:
                items = db.query(models.Item).limit(top_k).all()
            
            return items
        
        # Search similar items
        distances, indices = self.index.search(user_emb, top_k * 2)  # Get more to filter
        
        # Filter out items user already interacted with
        interacted_ids = set([
            i.item_id for i in db.query(models.UserInteraction).filter(
                models.UserInteraction.user_id == user_id
            ).all()
        ])
        
        recommended_items = []
        for idx in indices[0]:
            item_id = self.item_ids[idx]
            if item_id not in interacted_ids:
                item = db.query(models.Item).filter(models.Item.id == item_id).first()
                if item:
                    recommended_items.append(item)
                if len(recommended_items) >= top_k:
                    break
        
        return recommended_items
