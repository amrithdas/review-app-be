from django.urls import path
from .views import create_review, get_reviews

urlpatterns = [
    path('api/create_review/', create_review, name='create_review'),
    path('api/get_reviews/', get_reviews, name='get_reviews'),
]