// Script for Healthy Meal Planner

document.addEventListener('DOMContentLoaded', function() {
    console.log('Healthy Meal Planner loaded');
    
    // Add hover effects to recipe cards
    const recipeCards = document.querySelectorAll('.recipe-card');
    
    recipeCards.forEach(card => {
        card.addEventListener('click', function() {
            console.log('Recipe card clicked');
            
            // Future:  Navigate to recipe detail page
        });
    });
    
    // Search form enhancement
    const searchForm = document. querySelector('.search-form');
    
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = document.querySelector('.search-input');
            if (searchInput. value.trim() === '') {
                e.preventDefault();
                alert('Please enter a search term');
            }
        });
    }
});