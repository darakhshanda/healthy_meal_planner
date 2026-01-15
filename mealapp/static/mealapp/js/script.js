// Script for Healthy Meal Planner

// Recipe Grid Functionality
let allRecipes = [];
let currentCategory = 'all';
let currentPage = 1;
const recipesPerPage = 12;

function initializeRecipeGrid() {
    // Get recipes data from the template
    const recipesDataElement = document.getElementById('recipesData');
    if (recipesDataElement) {
        try {
            allRecipes = JSON.parse(recipesDataElement.textContent);
            console.log(`✅ Loaded ${allRecipes.length} recipes`);
            currentPage = 1; // Reset to first page
            displayRecipes();
        } catch (e) {
            console.error('❌ Error parsing recipes data:', e);
        }
    }
}

function getFilteredRecipes() {
    let filtered = allRecipes;

    // Filter by category
    if (currentCategory !== 'all') {
        filtered = filtered.filter(r => r.category === currentCategory);
    }

    return filtered;
}

function displayRecipes() {
    const container = document.getElementById('recipesContainer');
    if (!container) return;
    
    container.innerHTML = '';

    // Get filtered recipes
    const filteredRecipes = getFilteredRecipes();
    
    // Calculate pagination
    const totalPages = Math.ceil(filteredRecipes.length / recipesPerPage);
    const startIndex = (currentPage - 1) * recipesPerPage;
    const endIndex = startIndex + recipesPerPage;
    const recipesToDisplay = filteredRecipes.slice(startIndex, endIndex);

    // Display recipes for current page
    recipesToDisplay.forEach(recipe => {
        const card = createRecipeCard(recipe);
        container.appendChild(card);
    });

    // Update count
    const countElement = document.getElementById('recipeCount');
    if (countElement) {
        const startNum = filteredRecipes.length === 0 ? 0 : startIndex + 1;
        const endNum = Math.min(endIndex, filteredRecipes.length);
        countElement.textContent = `Showing ${startNum}-${endNum} of ${filteredRecipes.length} recipe${filteredRecipes.length !== 1 ? 's' : ''}`;
    }

    // Update pagination UI
    updatePaginationUI(totalPages, filteredRecipes.length);
}

function updatePaginationUI(totalPages, totalRecipes) {
    // Hide pagination if only one page or no results
    const paginationNav = document.querySelector('.pagination-nav');
    if (paginationNav) {
        if (totalPages <= 1 || totalRecipes === 0) {
            paginationNav.style.display = 'none';
        } else {
            paginationNav.style.display = 'block';
        }
    }

    // Update pagination links (if they exist)
    const prevLink = document.querySelector('.pagination .page-item:first-child a');
    const nextLink = document.querySelector('.pagination .page-item:last-child a');
    const pageInfo = document.querySelector('.pagination .page-link:not([href])');

    if (prevLink) {
        if (currentPage > 1) {
            prevLink.href = '#';
            prevLink.onclick = (e) => { e.preventDefault(); changePage(currentPage - 1); };
        }
    }

    if (nextLink) {
        if (currentPage < totalPages) {
            nextLink.href = '#';
            nextLink.onclick = (e) => { e.preventDefault(); changePage(currentPage + 1); };
        }
    }

    if (pageInfo) {
        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    }
}

function changePage(page) {
    const filteredRecipes = getFilteredRecipes();
    const totalPages = Math.ceil(filteredRecipes.length / recipesPerPage);
    
    if (page >= 1 && page <= totalPages) {
        currentPage = page;
        displayRecipes();
        // Scroll to top of recipes section
        document.querySelector('.recipes-section')?.scrollIntoView({ behavior: 'smooth' });
    }
}

function createRecipeCard(recipe) {
    const card = document.createElement('div');
    card.className = 'recipe-card active';

    const ingredientsList = (recipe.ingredients || [])
        .slice(0, 6)
        .map(ing => {
            const ingName = typeof ing === 'string' ? ing : ing.name || '';
            return ingName ? `<li>${ingName}</li>` : '';
        })
        .join('');

    const instructionsList = (recipe.instructions || []).slice(0, 1).map(inst => {
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
                    ${ingredientsList}
                </ul>
            </div>
            ` : ''}    
            <a href="/recipe/${recipe.id}/" class="btn">View Recipe</a>
        </div>
    `;

    return card;
}
function displayRecipe(recipe) {
    const card = document.createElement('div');
    card.className = 'recipe-card active';

    const ingredientsList = (recipe.ingredients || [])
        .slice(0, 6)
        .map(ing => {
            const ingName = typeof ing === 'string' ? ing : ing.name || '';
            return ingName ? `<li>${ingName}</li>` : '';
        })
        .join('');

    const instructionsList = (recipe.instructions || []).slice(0, 1).map(inst => {
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
                    ${ingredientsList}
                </ul>
            </div>
            ` : ''}       
             ${ingredientsList ? `
            <div class="ingredients-section">
                <div class="section-title">Key Ingredients</div>
                <ul class="ingredients-list">
                    ${ingredientsList}
                </ul>
            </div>
            ` : ''}    
             ${ingredientsList ? `
            <div class="ingredients-section">
                <div class="section-title">Key Ingredients</div>
                <ul class="ingredients-list">
                    ${ingredientsList}
                </ul>
            </div>
            ` : ''}    
             ${ingredientsList ? `
            <div class="ingredients-section">
                <div class="section-title">Key Ingredients</div>
                <ul class="ingredients-list">
                    ${ingredientsList}
                </ul>
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
            currentPage = 1; // Reset to first page when changing category
            displayRecipes();
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