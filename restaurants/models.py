from django.db import models
from django.contrib.postgres.fields import ArrayField

class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    contact_info = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    cafe = models.BooleanField(default=False)
    bakery = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    reviews = models.IntegerField(blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    opening_time = models.TimeField(blank=True, null=True)
    closing_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    veg = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class RestaurantReview(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    food_quality_rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    service_rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    ambiance_rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.restaurant.name} by {self.user_name}"