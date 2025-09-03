# Smart Recipe Recommendation API

A recipe recommendation system that suggests personalized recipes based on ingredients, dietary preferences, and cooking skills.

## Features

- **Ingredient-Based Search**: Find recipes using available ingredients
- **AI-Powered Recommendations**: Get personalized recipe suggestions using OpenAI
- **Dietary Filters**: Support for vegetarian, vegan, gluten-free, and other dietary restrictions
- **Difficulty Levels**: Recipes categorized by cooking skill level
- **Nutritional Information**: Basic nutritional data for each recipe
- **Recipe Rating System**: Users can rate and review recipes

## Tech Stack

- **Backend**: FastAPI with async support
- **Database**: SQLite (lightweight and portable)
- **AI Integration**: OpenAI GPT API for recipe recommendations
- **Data Validation**: Pydantic models

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and add your OpenAI API key
3. Initialize the database:
   ```bash
   python setup_db.py
   ```
4. Start the server:
   ```bash
   python start.py
   ```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.



```
├── main.py              # FastAPI application
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── database.py          # Database configuration
├── recipe_service.py    # Recipe recommendation logic
└── static/              # Frontend files
