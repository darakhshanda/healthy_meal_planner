
// RECIPE GRID FUNCTIONALITY


let allRecipes = [];
let currentCategory = 'all';
let currentPage = 1;
const recipesPerPage = 12; // 3 cards in 4 rows

function initializeRecipeGrid() {
    const recipesDataElement = document.getElementById('recipesData');
    if (recipesDataElement) {
        try {
            allRecipes = JSON.parse(recipesDataElement.textContent);
            console.log(`Loaded ${allRecipes.length} recipes`);
            currentPage = 1;
            displayRecipes();
        } catch (e) {
            console.error('❌ Error parsing recipes data:', e);
        }
    }
}
// Filter recipes by category
function getFilteredRecipes() {
    let filtered = allRecipes;
    if (currentCategory !== 'all') {
        filtered = filtered.filter(r => r.category === currentCategory);
    }
    return filtered;
}
// Display recipes in grid
function displayRecipes() {
    const container = document.getElementById('recipesContainer');
    if (!container) return;
    
    container.innerHTML = '';
    const filteredRecipes = getFilteredRecipes();
    const totalPages = Math.ceil(filteredRecipes.length / recipesPerPage);
    const startIndex = (currentPage - 1) * recipesPerPage;
    const endIndex = startIndex + recipesPerPage;
    const recipesToDisplay = filteredRecipes.slice(startIndex, endIndex);

    if (recipesToDisplay.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="alert alert-info text-center">
                    <i class="fas fa-info-circle"></i> No recipes found.
                </div>
            </div>
        `;
    } else {
        recipesToDisplay.forEach(recipe => {
            const cardColumn = createRecipeCard(recipe);
            container.appendChild(cardColumn);
        });
    }

    // Update count
    const countElement = document.getElementById('recipeCount');
    if (countElement) {
        const startNum = filteredRecipes.length === 0 ? 0 : startIndex + 1;
        const endNum = Math.min(endIndex, filteredRecipes.length);
        countElement.textContent = `Showing ${startNum}-${endNum} of ${filteredRecipes.length} recipes`;
    }

    updatePaginationUI(totalPages, filteredRecipes.length);
}

function createRecipeCard(recipe) {
    // Create column wrapper for grid layout
    const col = document.createElement('div');
    col.className = 'col'; // Bootstrap will handle sizing based on row-cols-*

    // Create card
    const card = document.createElement('div');
    card.className = 'card recipe-card shadow-lg h-100';

    // Build card content
    card.innerHTML = `
        ${recipe.image_url ? `
            <img src="${recipe.image_url}" alt="${recipe.title}" class="recipe-image" 
                 onerror="this.onerror=null;this.src='/static/mealapp/images/default.jpg';" />
        ` : `
            <div class="recipe-image-placeholder">
                <i class="fas fa-utensils fa-3x text-white"></i>
            </div>
        `}
        
        <div class="card-body d-flex flex-column">
            <!-- Title & Category -->
            <div class="mb-3">
                <h5 class="card-title fw-bold">${recipe.title}</h5>
                <span class="badge bg-primary">${recipe.category}</span>
            </div>

            <!-- Description -->
            <p class="card-text text-muted flex-grow-1">
                ${recipe.description ? recipe.description.substring(0, 100) + '...' : 'No description available'}
            </p>

            <!-- Nutrition Info -->
            <div class="nutrition-info mb-3">
                <div class="row text-center">
                    <div class="col-6">
                        <small class="text-muted d-block">Calories</small>
                        <p class="mb-0 fw-bold">${recipe.total_calories || '--'}</p>
                    </div>
                    <div class="col-6">
                        <small class="text-muted d-block">Servings</small>
                        <p class="mb-0 fw-bold">${recipe.servings || '--'}</p>
                    </div>
                </div>
                <hr class="my-2">
                <div class="row text-center small">
                    <div class="col-4">
                        <i class="fas fa-drumstick-bite text-danger"></i>
                        <p class="mb-0">${recipe.protein || 0}g</p>
                    </div>
                    <div class="col-4">
                        <i class="fas fa-bread-slice text-warning"></i>
                        <p class="mb-0">${recipe.carbs || 0}g</p>
                    </div>
                    <div class="col-4">
                        <i class="fas fa-bacon text-info"></i>
                        <p class="mb-0">${recipe.fat || 0}g</p>
                    </div>
                </div>
            </div>

            <!-- Time Info -->
            <div class="mb-3">
                <small class="text-muted">
                    <i class="fas fa-clock"></i> 
                    ${recipe.prep_time_minutes ? `Prep: ${recipe.prep_time_minutes}m` : ''} 
                    ${recipe.cook_time_minutes ? `| Cook: ${recipe.cook_time_minutes}m` : ''}
                </small>
            </div>

            <!-- Creator -->
            <small class="text-muted mb-3">
                By <strong>${recipe.created_by || 'Unknown'}</strong>
            </small>

            <!-- Action Button -->
            <a href="/recipes/${recipe.id}/" class="btn btn-primary w-100 mt-auto">
                <i class="fas fa-eye"></i> View Recipe
            </a>
        </div>
    `;

    col.appendChild(card);
    return col;
}

function updatePaginationUI(totalPages, totalRecipes) {
    const paginationNav = document.querySelector('.pagination-nav');
    const pageInfo = document.getElementById('pageInfo');

    if (paginationNav && pageInfo) {
        if (totalPages <= 1 || totalRecipes === 0) {
            paginationNav.style.display = 'none';
        } else {
            paginationNav.style.display = 'block';
            pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;

            // Update previous button
            const prevButton = paginationNav.querySelector('li:first-child');
            if (currentPage === 1) {
                prevButton.classList.add('disabled');
            } else {
                prevButton.classList.remove('disabled');
            }

            // Update next button
            const nextButton = paginationNav.querySelector('li:last-child');
            if (currentPage === totalPages) {
                nextButton.classList.add('disabled');
            } else {
                nextButton.classList.remove('disabled');
            }
        }
    }
}

function changePage(page) {
    const filteredRecipes = getFilteredRecipes();
    const totalPages = Math.ceil(filteredRecipes.length / recipesPerPage);
    
    if (page >= 1 && page <= totalPages) {
        currentPage = page;
        displayRecipes();
        document.querySelector('.recipes-section')?.scrollIntoView({ behavior: 'smooth' });
    }
}


// FORM VALIDATION


function validateForm(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return true;

    return form.checkValidity() === false ? false : true;
}

// INITIALIZATION


document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Healthy Meal Planner loaded');
    
    // Initialize recipe grid
    initializeRecipeGrid();

    // Category filter
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', (e) => {
            document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            currentCategory = e.target.dataset.category;
            currentPage = 1;
            displayRecipes();
        });
    });

    // Bootstrap form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});