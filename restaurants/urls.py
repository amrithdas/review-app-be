from django.urls import path
from .views import create_restaurant, create_restaurantreview, get_bakeries, get_cafes, get_fooditems, get_restaurants, nonveg_restaurants, open_restaurants, restaurant_reviews, veg_restaurants

urlpatterns = [
    path('api/get-restaurants/', get_restaurants, name='get_restaurants'),
    path('api/create-restaurant/', create_restaurant, name='create_restaurant'),
    path('api/food-items/', get_fooditems, name='get_fooditems'),
    path('api/open-restaurants/', open_restaurants, name='open_restaurants'),
    path('api/veg-restaurants/', veg_restaurants, name='veg_restaurants'),
    path('api/non-veg-restaurants/', nonveg_restaurants, name='non_veg_restaurants'),
    path('api/cafes/', get_cafes, name='get_cafes'),
    path('api/bakeries/', get_bakeries, name='get_bakeries'),
    path('api/restaurantreviews/', create_restaurantreview, name='create_restaurantreview'),
    path('api/restaurants/<int:restaurant_id>/reviews/', restaurant_reviews, name='restaurant_reviews'),
]
