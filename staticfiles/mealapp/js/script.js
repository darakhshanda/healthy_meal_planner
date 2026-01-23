/* jshint esversion: 6 */



// MEAL PLAN DATE SELECTION
document.getElementById('createMealPlanForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const date = document.getElementById('date').value;
    if (date) {
        window.location.href = '/meal-plan/' + date + '/';
    }
});
