from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('Logout/', views.Logout, name='Logout'),
    path('register/', views.register, name='register'),
    
    
]