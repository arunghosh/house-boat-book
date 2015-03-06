from django.db import models
from order.models import Order
from util.models import AutoDateAddModel

class ReviewManager(models.Manager):

    def get_for_boat(self, boat_id):
        reviews = self.get_queryset().filter(order__boat__id=boat_id, is_deleted=False)
        return reviews


class Review(AutoDateAddModel):
    order = models.ForeignKey(Order, related_name="reviews")
    comment = models.CharField(max_length=512)
    cleanliness = models.PositiveSmallIntegerField()
    food = models.PositiveSmallIntegerField()
    ambience = models.PositiveSmallIntegerField()
    is_deleted = models.BooleanField(default=False)

    @property
    def avg(self):
        return (self.food + self.ambience + self.cleanliness) / 3

    objects = ReviewManager()

# class ReviewReply(models.Model):