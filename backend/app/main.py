from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import recommendations, interactions, saved
import os

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Recommender SaaS API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-url.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recommendations.router)
app.include_router(interactions.router)
app.include_router(saved.router)

@app.get("/")
async def root():
    return {"message": "AI Recommender System API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
