from django.urls import path
from . import views


urlpatterns = [
    # Home & Profile
    path('', views.index, name='index'),
    path('profile/', views.profile_setup, name='profile_setup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('help/', views.help_page, name='help'),
    # Recipe CRUD
    path('recipes/create/', views.RecipeCreateView.as_view(), name='recipe_create'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:pk>/edit/',
         views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipes/<int:pk>/delete/',
         views.RecipeDeleteView.as_view(), name='recipe_delete'),

    # Meal Plan

    path('meal-plans/', views.meal_plan_list_view, name='meal_plan_list'),
    path('meal-plan/<int:plan_id>/',
         views.meal_plan_current, name='meal_plan_current'),
    path('meal-plan/create/', views.create_meal_plan, name='meal_plan_create'),
    path('meal-plan/<str:date>/', views.meal_plan_view, name='meal_plan_view'),
    path('meal-plan/<int:plan_id>/update/',
         views.meal_plan_update, name='meal_plan_update'),
    path('meal-plan/<int:plan_id>/delete/',
         views.delete_meal_plan, name='meal_plan_delete'),

]
