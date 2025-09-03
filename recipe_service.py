from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
import openai
import json
import os
from dotenv import load_dotenv
from models import Recipe, Rating
from schemas import RecipeCreate, RecipeRecommendation

load_dotenv()

class RecipeService:
    @staticmethod
    def create_recipe(db: Session, recipe: RecipeCreate) -> Recipe:
        db_recipe = Recipe(**recipe.dict())
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        return db_recipe

    @staticmethod
    def get_recipe(db: Session, recipe_id: int) -> Optional[Recipe]:
        return db.query(Recipe).filter(Recipe.id == recipe_id).first()

    @staticmethod
    def search_recipes(
        db: Session, 
        ingredients: Optional[str] = None,
        dietary_restriction: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> List[Recipe]:
        query = db.query(Recipe)
        
        if ingredients:
            # Simple ingredient search
            ingredient_list = [ing.strip().lower() for ing in ingredients.split(',')]
            for ingredient in ingredient_list:
                query = query.filter(Recipe.ingredients.contains(ingredient))
        
        if dietary_restriction:
            query = query.filter(Recipe.dietary_restrictions.contains(dietary_restriction))
        
        if difficulty:
            query = query.filter(Recipe.difficulty == difficulty)
        
        return query.limit(20).all()

    @staticmethod
    def rate_recipe(db: Session, recipe_id: int, rating: int, comment: str = None, user_name: str = "Anonymous"):
        db_rating = Rating(
            recipe_id=recipe_id,
            rating=rating,
            comment=comment,
            user_name=user_name
        )
        db.add(db_rating)
        db.commit()
        return db_rating

    @staticmethod
    def get_popular_recipes(db: Session, limit: int = 10) -> List[Recipe]:
        # Get recipes with highest average ratings
        subquery = db.query(
            Rating.recipe_id,
            func.avg(Rating.rating).label('avg_rating'),
            func.count(Rating.id).label('rating_count')
        ).group_by(Rating.recipe_id).subquery()
        
        return db.query(Recipe).join(
            subquery, Recipe.id == subquery.c.recipe_id
        ).filter(
            subquery.c.rating_count >= 2  # At least 2 ratings
        ).order_by(
            desc(subquery.c.avg_rating)
        ).limit(limit).all()

    @staticmethod
    async def get_ai_recommendations(
        db: Session,
        ingredients: str,
        dietary_preferences: Optional[str] = None,
        skill_level: str = "beginner"
    ) -> List[RecipeRecommendation]:
        """Get AI-powered recipe recommendations"""
        
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            # Return sample recommendations if no API key
            return RecipeService._get_sample_recommendations(ingredients)
        
        try:
            openai.api_key = openai_api_key
            
            prompt = f"""
            Based on these available ingredients: {ingredients}
            Dietary preferences: {dietary_preferences or 'None'}
            Cooking skill level: {skill_level}
            
            Suggest 3 creative and practical recipes. For each recipe, provide:
            - Title
            - Brief description
            - List of ingredients (including the ones provided)
            - Step-by-step instructions
            - Estimated prep time in minutes
            - Difficulty level (easy/medium/hard)
            - Why this recipe is recommended for these ingredients
            
            Format as JSON array with this structure:
            [{{
                "title": "Recipe Name",
                "description": "Brief description",
                "ingredients": ["ingredient1", "ingredient2"],
                "instructions": ["step1", "step2"],
                "prep_time": 30,
                "difficulty": "easy",
                "why_recommended": "Explanation"
            }}]
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful cooking assistant that suggests creative recipes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.8
            )
            
            content = response.choices[0].message.content
            recipes_data = json.loads(content)
            
            return [RecipeRecommendation(**recipe) for recipe in recipes_data]
            
        except Exception as e:
            print(f"AI recommendation error: {e}")
            return RecipeService._get_sample_recommendations(ingredients)

    @staticmethod
    def _get_sample_recommendations(ingredients: str) -> List[RecipeRecommendation]:
        """Fallback sample recommendations when AI is unavailable"""
        ingredient_list = [ing.strip() for ing in ingredients.split(',')]
        
        return [
            RecipeRecommendation(
                title=f"Simple {ingredient_list[0].title()} Stir-fry",
                description=f"A quick and easy stir-fry featuring {ingredient_list[0]}",
                ingredients=ingredient_list + ["soy sauce", "garlic", "oil"],
                instructions=[
                    "Heat oil in a pan",
                    f"Add {ingredient_list[0]} and cook for 5 minutes",
                    "Add garlic and soy sauce",
                    "Stir-fry for 3 more minutes",
                    "Serve hot"
                ],
                prep_time=15,
                difficulty="easy",
                why_recommended=f"Perfect for using {ingredient_list[0]} in a simple, healthy dish"
            ),
            RecipeRecommendation(
                title="Mixed Ingredient Soup",
                description="A hearty soup using your available ingredients",
                ingredients=ingredient_list + ["broth", "onion", "salt", "pepper"],
                instructions=[
                    "Sauté onion until soft",
                    "Add your ingredients and broth",
                    "Simmer for 20 minutes",
                    "Season with salt and pepper",
                    "Serve warm"
                ],
                prep_time=30,
                difficulty="easy",
                why_recommended="Great way to combine multiple ingredients into a comforting meal"
            )
        ]
