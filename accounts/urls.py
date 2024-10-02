from django.urls import path
from . import views

urlpatterns = [
    path('csrf/', views.get_csrf, name='api-csrf'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('check-auth/', views.check_auth_status, name='check-auth-status'),
    path('logout/', views.user_logout, name='logout'),
    path('google-login/', views.google_login, name='google-login'),
    path('profile/', views.get_user_profile, name='get_user_profile'),
]