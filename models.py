from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    ingredients = Column(Text, nullable=False)  
    instructions = Column(Text, nullable=False)
    prep_time = Column(Integer)  
    cook_time = Column(Integer)  
    servings = Column(Integer)
    difficulty = Column(String) 
    dietary_restrictions = Column(String)  
    cuisine_type = Column(String)
    calories_per_serving = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    ratings = relationship("Rating", back_populates="recipe")

    @property
    def average_rating(self):
        if not self.ratings:
            return 0
        return sum(r.rating for r in self.ratings) / len(self.ratings)


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text)
    user_name = Column(String)  # Simple user identification
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    recipe = relationship("Recipe", back_populates="ratings")
