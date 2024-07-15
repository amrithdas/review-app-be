from django.contrib import admin
from .models import FoodItem, Restaurant, RestaurantReview

admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(RestaurantReview)