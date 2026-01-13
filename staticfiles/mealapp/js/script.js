// mealapp/static/mealapp/js/script.js
document.addEventListener('DOMContentLoaded', () => {
        // Recipe data
        const recipes = {
            breakfast: [],
            lunch: [],
            dinner: []
        };

        let allRecipes = [];
        let currentCategory = 'all';
        let searchTerm = '';

        // Fetch and load recipes
        async function loadRecipes() {
            try {
                const categories = ['breakfast', 'lunch', 'dinner'];

                for (const category of categories) {
                    const filename = `${category}_recipes.json`;
                    const response = await fetch(filename);
                    const data = await response.json();
                    recipes[category] = data.map(recipe => ({
                        ...recipe,
                        category: category
                    }));
                    allRecipes.push(...recipes[category]);
                }

                displayRecipes();
            } catch (error) {
                console.error('Error loading recipes:', error);
                document.getElementById('recipesContainer').innerHTML =
                    '<p style="color: white; text-align: center;">Error loading recipes. Make sure JSON files are in the same directory.</p>';
            }
        }

        function displayRecipes() {
            const container = document.getElementById('recipesContainer');
            container.innerHTML = '';

            let recipesToDisplay = allRecipes;

            // Filter by category
            if (currentCategory !== 'all') {
                recipesToDisplay = recipesToDisplay.filter(r => r.category === currentCategory);
            }

            // Filter by search term
            if (searchTerm) {
                recipesToDisplay = recipesToDisplay.filter(recipe =>
                    recipe.recipe_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                    recipe.ingredients.some(ing => ing.toLowerCase().includes(searchTerm.toLowerCase()))
                );
            }

            recipesToDisplay.forEach(recipe => {
                const card = createRecipeCard(recipe);
                container.appendChild(card);
            });

            // Update count
            document.getElementById('recipeCount').textContent =
                `Showing ${recipesToDisplay.length} recipe${recipesToDisplay.length !== 1 ? 's' : ''}`;
        }

        function createRecipeCard(recipe) {
            const card = document.createElement('div');
            card.className = 'recipe-card active';

            const ingredientsList = recipe.ingredients
                .slice(0, 6)
                .map(ing => `<li>${ing}</li>`)
                .join('');

            const instructionsList = recipe.instructions
                .slice(0, 3)
                .map(inst => {
                    // Remove step markers if present
                    const cleanInst = inst.replace(/^step\s+\d+\s*:?\s*/i, '').trim();
                    return cleanInst ? `<li>${cleanInst}</li>` : '';
                })
                .join('');

            card.innerHTML = `
                <img src="${recipe.image_url}" alt="${recipe.recipe_name}" class="recipe-image" 
                     onerror="this.src='https://via.placeholder.com/300x200?text=Recipe+Image'">
                <div class="recipe-content">
                    <div class="recipe-name">${recipe.recipe_name}</div>
                    
                    <div class="recipe-info-bar">
                        <div class="info-badge">👥 Servings: ${recipe.servings || 2}</div>
                    </div>
                    
                    <div class="ingredients-section">
                        <div class="section-title">Key Ingredients</div>
                        <ul class="ingredients-list">
                            ${ingredientsList}
                        </ul>
                    </div>

                    <div class="instructions-section">
                        <div class="section-title">Steps</div>
                        <ol class="instructions-list">
                            ${instructionsList}
                        </ol>
                    </div>

                    <div class="recipe-stats">
                        <div class="stat-item">
                            <span>📝</span>
                            <span>${recipe.ingredients.length} ingredients</span>
                        </div>
                        <div class="stat-item">
                            <span>👨‍🍳</span>
                            <span>${recipe.instructions.length} steps</span>
                        </div>
                    </div>
                </div>
            `;

            return card;
        }

        // Event listeners
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', (e) => {
                document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                currentCategory = e.target.dataset.category;
                displayRecipes();
            });
        });

        document.getElementById('searchInput').addEventListener('input', (e) => {
            searchTerm = e.target.value;
            displayRecipes();
        });

        // Load recipes on page load
        loadRecipes();
    });
