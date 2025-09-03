from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
from database import get_db, init_db
from models import Recipe, Rating
from schemas import RecipeCreate, RecipeResponse, RatingCreate, RecipeRecommendation
from recipe_service import RecipeService
from sqlalchemy.orm import Session
from fastapi import Depends

app = FastAPI(
    title="Smart Recipe Recommendation API",
    description="AI-powered recipe recommendations based on ingredients and preferences",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {
        "message": "Welcome to Smart Recipe Recommendation API",
        "docs": "/docs",
        "frontend": "/static/index.html"
    }

@app.get("/recipes/", response_model=List[RecipeResponse])
async def get_recipes(
    ingredients: Optional[str] = Query(None, description="Comma-separated ingredients"),
    dietary_restriction: Optional[str] = Query(None, description="vegetarian, vegan, gluten-free"),
    difficulty: Optional[str] = Query(None, description="easy, medium, hard"),
    db: Session = Depends(get_db)
):
    """Get recipes filtered by ingredients, dietary restrictions, and difficulty"""
    return RecipeService.search_recipes(db, ingredients, dietary_restriction, difficulty)

@app.post("/recipes/", response_model=RecipeResponse)
async def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    """Create a new recipe"""
    return RecipeService.create_recipe(db, recipe)

@app.get("/recipes/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Get a specific recipe by ID"""
    recipe = RecipeService.get_recipe(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.post("/recipes/{recipe_id}/rate")
async def rate_recipe(recipe_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    """Rate a recipe"""
    return RecipeService.rate_recipe(db, recipe_id, rating.rating, rating.comment)

@app.get("/recommendations/", response_model=List[RecipeRecommendation])
async def get_ai_recommendations(
    ingredients: str = Query(..., description="Available ingredients"),
    dietary_preferences: Optional[str] = Query(None, description="Dietary preferences"),
    skill_level: Optional[str] = Query("beginner", description="Cooking skill level"),
    db: Session = Depends(get_db)
):
    """Get AI-powered recipe recommendations"""
    return await RecipeService.get_ai_recommendations(db, ingredients, dietary_preferences, skill_level)

@app.get("/recipes/popular/", response_model=List[RecipeResponse])
async def get_popular_recipes(limit: int = Query(10, le=50), db: Session = Depends(get_db)):
    """Get most popular recipes based on ratings"""
    return RecipeService.get_popular_recipes(db, limit)
