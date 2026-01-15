// Script for Healthy Meal Planner

// Recipe Grid Functionality
let allRecipes = [];
let currentCategory = 'all';
let searchTerm = '';

function initializeRecipeGrid() {
    // Get recipes data from the template
    const recipesDataElement = document.getElementById('recipesData');
    if (recipesDataElement) {
        try {
            allRecipes = JSON.parse(recipesDataElement.textContent);
            console.log(`✅ Loaded ${allRecipes.length} recipes`);
            displayRecipes();
        } catch (e) {
            console.error('❌ Error parsing recipes data:', e);
        }
    }
}

function displayRecipes() {
    const container = document.getElementById('recipesContainer');
    if (!container) return;
    
    container.innerHTML = '';

    let recipesToDisplay = allRecipes;

    // Filter by category
    if (currentCategory !== 'all') {
        recipesToDisplay = recipesToDisplay.filter(r => r.category === currentCategory);
    }

    // Filter by search term (client-side for instant feedback)
    if (searchTerm) {
        recipesToDisplay = recipesToDisplay.filter(recipe =>
            recipe.recipe_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (recipe.ingredients && recipe.ingredients.some(ing =>
                ing.toLowerCase().includes(searchTerm.toLowerCase())
            ))
        );
    }

    recipesToDisplay.forEach(recipe => {
        const card = createRecipeCard(recipe);
        container.appendChild(card);
    });

    // Update count
    const countElement = document.getElementById('recipeCount');
    if (countElement) {
        countElement.textContent =
            `Showing ${recipesToDisplay.length} recipe${recipesToDisplay.length !== 1 ? 's' : ''}`;
    }
}

function createRecipeCard(recipe) {
    const card = document.createElement('div');
    card.className = 'recipe-card active';

    const ingredientsList = (recipe.ingredients.name || [])
        .slice(0, 6)
        .map(ing => `<li>${ing}</li>`)
        .join('');

    const instructionsList = (recipe.instructions || [])
        .slice(0, 3)
        .map(inst => {
            const cleanInst = inst.replace(/^step\s+\d+\s*:?\s*/i, '').trim();
            return cleanInst ? `<li>${cleanInst}</li>` : '';
        })
        .join('');

    card.innerHTML = `
        <img src="${recipe.image_url}" alt="${recipe.recipe_name}" class="recipe-image" 
             onerror="this.onerror=null;this.src='/static/mealapp/images/default.jpg';" />
        <div class="recipe-content">
            <div class="recipe-name">${recipe.recipe_name}</div>
            
            <div class="recipe-info-bar">
                <div class="info-badge">👥 ${recipe.servings || 2} servings</div>
                <div class="info-badge">⏱️ ${recipe.prep_time_minutes} min</div>
                <div class="info-badge">🔥 ${recipe.total_calories} cal</div>
            </div>
            
            ${ingredientsList ? `
            <div class="ingredients-section">
                <div class="section-title">Key Ingredients</div>
                <ul class="ingredients-list">
                    ${ingredientsList.name}
                </ul>
            </div>
            ` : ''}

            ${instructionsList ? `
            <div class="instructions-section">
                <div class="section-title">Steps</div>
                <ol class="instructions-list">
                    ${instructionsList}
                </ol>
            </div>
            ` : ''}

            <a href="/recipe/${recipe.id}/" class="btn">View Recipe</a>
        </div>
    `;

    return card;
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Healthy Meal Planner loaded');
    
    // Initialize recipe grid
    initializeRecipeGrid();

    // Event listeners for category tabs
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', (e) => {
            document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentCategory = e.target.dataset.category;
            displayRecipes();
        });
    });

    // Add hover effects to recipe cards
    const recipeCards = document.querySelectorAll('.recipe-card');
    console.log(`✅ Found ${recipeCards.length} recipe cards`);

    recipeCards.forEach(card => {
        card.addEventListener('click', function() {
            console.log('Recipe card clicked');
            // Future:  Navigate to recipe detail page
        });
    });

      
    // Search form enhancement
    const searchForm = document.querySelector('.search-form');
    
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = document.querySelector('.search-input');
            if (searchInput.value.trim() === '') {
                e.preventDefault();
                alert('Please enter a search term');
            }
        });
    }
});