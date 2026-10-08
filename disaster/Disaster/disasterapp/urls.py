from django.urls import path
from . import views
urlpatterns = [
    # Public Pages
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    # User Authentication & Dashboard
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    # Admin Authentication
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    # Admin Functionalities
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('run-prediction/', views.run_prediction, name='run_prediction'),
    # Optional: If you want a specific page to view all viewers separately
    path('admin-viewers/', views.admin_users, name='admin_viewers'),
]