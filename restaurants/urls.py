from django.urls import path
from . import views

urlpatterns = [
    path('api/get-restaurants/', views.get_restaurants, name='get_restaurants'),
    path('api/create-restaurant/', views.create_restaurant, name='create_restaurant'),
    path('api/food-items/', views.get_fooditems, name='get_fooditems'),
    path('api/open-restaurants/', views.open_restaurants, name='open_restaurants'),
    path('api/veg-restaurants/', views.veg_restaurants, name='veg_restaurants'),
    path('api/non-veg-restaurants/', views.nonveg_restaurants, name='non_veg_restaurants'),
    path('api/cafes/', views.get_cafes, name='get_cafes'),
    path('api/bakeries/', views.get_bakeries, name='get_bakeries'),
    path('api/createrestaurantreviews/', views.create_restaurantreview, name='create_restaurantreview'),
    path('api/restaurants/<str:restaurant_name>/reviews/', views.restaurant_reviews, name='restaurant_reviews'),
    path('api/restaurants/list', views.search_restaurants, name='search_businesses'),
    path('api/recent-reviews/', views.recent_reviews, name='recent-reviews'),
    path('api/restaurant/<str:restaurant_name>/', views.restaurant_details, name='restaurant-details'),
    path('api/<str:restaurant_name>/review_count/', views.review_count, name='review_count'),
]
