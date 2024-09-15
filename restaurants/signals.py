from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Restaurant, RestaurantReview

@receiver(post_save, sender=RestaurantReview)
@receiver(post_delete, sender=RestaurantReview)
def update_restaurant_rating(sender, instance, **kwargs):
    # Ensure `instance.restaurant_name` is the correct field
    restaurant_name = instance.restaurant_name
    restaurant = Restaurant.objects.filter(name=restaurant_name).first()
    if restaurant:
        reviews = RestaurantReview.objects.filter(restaurant_name=restaurant_name)
        if reviews.exists():
            average_rating = reviews.aggregate(average_rating=Avg('rating'))['average_rating']
            restaurant.rating = average_rating
            restaurant.save()
        else:
            restaurant.rating = None
            restaurant.save()
