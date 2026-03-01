# church/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('me/', views.me_view, name='me'),
    path('admin/', views.admin, name='admin'),
    path('pastor/', views.pastor_view, name='pastor'),
    path('church_admin/', views.church_admin_view, name='church_admin'),
    path('treasurer/', views.treasurer_view, name='treasurer'),
    path('dept_leader/', views.dept_leader_view, name='dept_leader'),
    path('403/', views.permission_denied_view, name='permission_denied'),
    #path('main/admin/', views.admin_view, name='admin'),
    
]