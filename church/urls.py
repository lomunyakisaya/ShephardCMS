# church/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('main/', views.main_view, name='main'),
    #path('main/prayers/', views.prayers_view, name='prayers'),
    path('profile/', views.profile_edit_view, name='edit_profile'),
    #path('main/prayers/add/', views.add_prayer_view, name='add_prayer'),
    #path('main/suggestions/', views.suggestions_view, name='suggestions'),
    #path('main/events/', views.events_view, name='events'),
    #path('main/not/', views.notifications, name='notifications'),
    path('main/leader/', views.leader_view, name='leader'),
    #path('main/admin/', views.admin_view, name='admin'),
    
]