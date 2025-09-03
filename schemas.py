from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None
    ingredients: str  # JSON string of ingredients list
    instructions: str
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: Optional[int] = None
    difficulty: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    cuisine_type: Optional[str] = None
    calories_per_serving: Optional[int] = None


class RecipeCreate(RecipeBase):
    pass


class RecipeResponse(RecipeBase):
    id: int
    average_rating: float
    created_at: datetime

    class Config:
        from_attributes = True


class RatingCreate(BaseModel):
    rating: int  # 1-5
    comment: Optional[str] = None
    user_name: Optional[str] = "Anonymous"


class RatingResponse(BaseModel):
    id: int
    rating: int
    comment: Optional[str]
    user_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class RecipeRecommendation(BaseModel):
    title: str
    description: str
    ingredients: List[str]
    instructions: List[str]
    prep_time: int
    difficulty: str
    why_recommended: str
