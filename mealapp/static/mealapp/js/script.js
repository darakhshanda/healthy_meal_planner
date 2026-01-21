


// FORM VALIDATION


function validateForm(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return true;

    return form.checkValidity() === false ? false : true;
}

// INITIALIZATION


document.addEventListener('DOMContentLoaded', function() {
    //console.log(' Healthy Meal Planner loaded');
    
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
// MEAL PLAN DATE SELECTION
document.getElementById('createMealPlanForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const date = document.getElementById('date').value;
    if (date) {
        window.location.href = '/meal-plan/' + date + '/';
    }
});
