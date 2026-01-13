from django.urls import path
from . import views

urlpatterns = [
    path('recipes/', views.recipe_list_view, name='recipe_list'),
]
