class RecipeApp {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.currentRecipeId = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadPopularRecipes();
    }

    setupEventListeners() {
        document.getElementById('search-form').addEventListener('submit', (e) => this.searchRecipes(e));
        document.getElementById('ai-recommend-btn').addEventListener('click', () => this.getAIRecommendations());
        document.getElementById('popular-btn').addEventListener('click', () => this.loadPopularRecipes());
        document.getElementById('add-recipe-form').addEventListener('submit', (e) => this.addRecipe(e));
        document.getElementById('submit-rating').addEventListener('click', () => this.submitRating());
    }

    showLoading() {
        document.getElementById('loading').style.display = 'block';
        document.getElementById('results-section').style.display = 'none';
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('results-section').style.display = 'block';
    }

    async searchRecipes(e) {
        e.preventDefault();
        const ingredients = document.getElementById('ingredients').value;
        const dietary = document.getElementById('dietary').value;
        
        if (!ingredients.trim()) {
            alert('Please enter some ingredients');
            return;
        }

        this.showLoading();
        
        try {
            const params = new URLSearchParams({
                ingredients: ingredients,
                ...(dietary && { dietary_restriction: dietary })
            });
            
            const response = await fetch(`${this.apiBase}/recipes/?${params}`);
            const recipes = await response.json();
            
            this.displayRecipes(recipes, `Recipes with: ${ingredients}`);
        } catch (error) {
            console.error('Search error:', error);
            alert('Failed to search recipes');
        } finally {
            this.hideLoading();
        }
    }

    async getAIRecommendations() {
        const ingredients = document.getElementById('ingredients').value;
        const dietary = document.getElementById('dietary').value;
        
        if (!ingredients.trim()) {
            alert('Please enter some ingredients first');
            return;
        }

        this.showLoading();
        
        try {
            const params = new URLSearchParams({
                ingredients: ingredients,
                ...(dietary && { dietary_preferences: dietary }),
                skill_level: 'beginner'
            });
            
            const response = await fetch(`${this.apiBase}/recommendations/?${params}`);
            const recommendations = await response.json();
            
            this.displayAIRecommendations(recommendations);
        } catch (error) {
            console.error('AI recommendation error:', error);
            alert('Failed to get AI recommendations');
        } finally {
            this.hideLoading();
        }
    }

    async loadPopularRecipes() {
        this.showLoading();
        
        try {
            const response = await fetch(`${this.apiBase}/recipes/popular/`);
            const recipes = await response.json();
            
            this.displayRecipes(recipes, 'Popular Recipes');
        } catch (error) {
            console.error('Failed to load popular recipes:', error);
            alert('Failed to load popular recipes');
        } finally {
            this.hideLoading();
        }
    }

    displayRecipes(recipes, title) {
        document.getElementById('results-title').textContent = title;
        const container = document.getElementById('recipes-container');
        container.innerHTML = '';

        if (recipes.length === 0) {
            container.innerHTML = '<div class="col-12"><p class="text-center text-muted">No recipes found. Try different ingredients!</p></div>';
            return;
        }

        recipes.forEach(recipe => {
            const recipeCard = this.createRecipeCard(recipe);
            container.appendChild(recipeCard);
        });
    }

    displayAIRecommendations(recommendations) {
        document.getElementById('results-title').textContent = 'AI Recommendations';
        const container = document.getElementById('recipes-container');
        container.innerHTML = '';

        if (recommendations.length === 0) {
            container.innerHTML = '<div class="col-12"><p class="text-center text-muted">No AI recommendations available.</p></div>';
            return;
        }

        recommendations.forEach(recipe => {
            const recipeCard = this.createAIRecipeCard(recipe);
            container.appendChild(recipeCard);
        });
    }

    createRecipeCard(recipe) {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4 mb-4';
        
        const ingredients = JSON.parse(recipe.ingredients || '[]');
        const ingredientTags = ingredients.slice(0, 3).map(ing => 
            `<span class="ingredient-tag">${ing}</span>`
        ).join('');
        
        const stars = '★'.repeat(Math.floor(recipe.average_rating)) + '☆'.repeat(5 - Math.floor(recipe.average_rating));
        
        col.innerHTML = `
            <div class="card recipe-card h-100">
                <div class="card-body">
                    <h5 class="card-title">${recipe.title}</h5>
                    <p class="card-text">${recipe.description || 'No description available'}</p>
                    <div class="mb-2">
                        ${ingredientTags}
                        ${ingredients.length > 3 ? `<span class="ingredient-tag">+${ingredients.length - 3} more</span>` : ''}
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            <i class="fas fa-clock"></i> ${recipe.prep_time || 'N/A'} min
                            <span class="ms-2">${recipe.difficulty || 'Easy'}</span>
                        </small>
                        <div class="rating-stars">
                            ${stars} (${recipe.average_rating.toFixed(1)})
                        </div>
                    </div>
                </div>
                <div class="card-footer">
                    <button class="btn btn-primary btn-sm w-100" onclick="app.viewRecipe(${recipe.id})">
                        <i class="fas fa-eye"></i> View Recipe
                    </button>
                </div>
            </div>
        `;
        
        return col;
    }

    createAIRecipeCard(recipe) {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4 mb-4';
        
        const ingredientTags = recipe.ingredients.slice(0, 3).map(ing => 
            `<span class="ingredient-tag">${ing}</span>`
        ).join('');
        
        col.innerHTML = `
            <div class="card recipe-card h-100 border-success">
                <div class="card-header bg-success text-white">
                    <i class="fas fa-robot"></i> AI Recommendation
                </div>
                <div class="card-body">
                    <h5 class="card-title">${recipe.title}</h5>
                    <p class="card-text">${recipe.description}</p>
                    <div class="mb-2">
                        ${ingredientTags}
                        ${recipe.ingredients.length > 3 ? `<span class="ingredient-tag">+${recipe.ingredients.length - 3} more</span>` : ''}
                    </div>
                    <div class="mb-2">
                        <small class="text-muted">
                            <i class="fas fa-clock"></i> ${recipe.prep_time} min
                            <span class="ms-2">${recipe.difficulty}</span>
                        </small>
                    </div>
                    <div class="alert alert-info p-2">
                        <small><strong>Why recommended:</strong> ${recipe.why_recommended}</small>
                    </div>
                </div>
                <div class="card-footer">
                    <button class="btn btn-success btn-sm w-100" onclick="app.viewAIRecipe(${JSON.stringify(recipe).replace(/"/g, '&quot;')})">
                        <i class="fas fa-eye"></i> View Recipe
                    </button>
                </div>
            </div>
        `;
        
        return col;
    }

    async viewRecipe(recipeId) {
        try {
            const response = await fetch(`${this.apiBase}/recipes/${recipeId}`);
            const recipe = await response.json();
            
            this.currentRecipeId = recipeId;
            this.showRecipeModal(recipe);
        } catch (error) {
            console.error('Failed to load recipe:', error);
            alert('Failed to load recipe details');
        }
    }

    viewAIRecipe(recipe) {
        this.currentRecipeId = null; // AI recipes don't have IDs
        this.showRecipeModal(recipe, true);
    }

    showRecipeModal(recipe, isAI = false) {
        document.getElementById('modal-recipe-title').textContent = recipe.title;
        
        const ingredients = isAI ? recipe.ingredients : JSON.parse(recipe.ingredients || '[]');
        const instructions = isAI ? recipe.instructions : recipe.instructions.split('\n');
        
        const content = `
            <div class="mb-3">
                <h6>Description</h6>
                <p>${recipe.description || 'No description available'}</p>
            </div>
            <div class="mb-3">
                <h6>Ingredients</h6>
                <ul>
                    ${ingredients.map(ing => `<li>${ing}</li>`).join('')}
                </ul>
            </div>
            <div class="mb-3">
                <h6>Instructions</h6>
                <ol>
                    ${instructions.map(inst => `<li>${inst}</li>`).join('')}
                </ol>
            </div>
            <div class="row">
                <div class="col-md-4">
                    <strong>Prep Time:</strong> ${recipe.prep_time || 'N/A'} minutes
                </div>
                <div class="col-md-4">
                    <strong>Difficulty:</strong> ${recipe.difficulty || 'Easy'}
                </div>
                <div class="col-md-4">
                    <strong>Servings:</strong> ${recipe.servings || 'N/A'}
                </div>
            </div>
        `;
        
        document.getElementById('modal-recipe-content').innerHTML = content;
        
        // Hide rating section for AI recipes
        const ratingSection = document.querySelector('.modal-footer .me-auto');
        ratingSection.style.display = isAI ? 'none' : 'block';
        
        const modal = new bootstrap.Modal(document.getElementById('recipeModal'));
        modal.show();
    }

    async submitRating() {
        if (!this.currentRecipeId) {
            alert('Cannot rate AI-generated recipes');
            return;
        }
        
        const rating = document.getElementById('rating-select').value;
        
        try {
            const response = await fetch(`${this.apiBase}/recipes/${this.currentRecipeId}/rate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    rating: parseInt(rating),
                    comment: '',
                    user_name: 'Anonymous'
                })
            });
            
            if (response.ok) {
                alert('Rating submitted successfully!');
                const modal = bootstrap.Modal.getInstance(document.getElementById('recipeModal'));
                modal.hide();
            }
        } catch (error) {
            console.error('Failed to submit rating:', error);
            alert('Failed to submit rating');
        }
    }

    async addRecipe(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        const ingredients = formData.get('ingredients').split(',').map(ing => ing.trim());
        
        try {
            const response = await fetch(`${this.apiBase}/recipes/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: formData.get('title'),
                    description: formData.get('description'),
                    ingredients: JSON.stringify(ingredients),
                    instructions: formData.get('instructions'),
                    prep_time: parseInt(formData.get('prep_time')) || null,
                    difficulty: formData.get('difficulty')
                })
            });
            
            if (response.ok) {
                alert('Recipe added successfully!');
                e.target.reset();
                this.loadPopularRecipes();
            }
        } catch (error) {
            console.error('Failed to add recipe:', error);
            alert('Failed to add recipe');
        }
    }
}

// Initialize the app
const app = new RecipeApp();
