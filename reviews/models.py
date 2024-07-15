from django.db import models
from django.utils.timezone import now

class Review(models.Model):
    name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, null=True)
    comment = models.TextField()
    individual_rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(default=now, blank=True)

    def __str__(self):
        return f"Review for {self.name} by {self.user_name}"
