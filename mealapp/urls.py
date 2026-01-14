from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('signup/', views.signup, name='signup'),  
    # path('login/', auth_views. LoginView.as_view(template_name='mealapp/login.html'), name='login'),
]
