from datetime import date
from django.db import models
from boat.models import Boat
from util.exception import InvalidFomToException, PastDateException
from util.models import AutoDateAddModel
from .exception import OrderExistException

class MaintenanceManager(models.Manager):

    def get_for_boat_id(self, boat_id):
        return self.get_queryset().filter(boat__id=boat_id)

    def get_for_date(self, p_date):
        objects = self.get_queryset().all()
        return [m for m in objects if m.date_from <= p_date <= m.date_to]


class Maintenance(AutoDateAddModel):
    boat = models.ForeignKey(Boat, related_name="maintenance")
    date_from = models.DateField()
    date_to = models.DateField()

    objects = MaintenanceManager()

    def save(self, *args, **kwargs):
        if self.date_from > self.date_to:
            raise InvalidFomToException
        if self.date_from < date.today():
            raise PastDateException
        if len(self.boat.orders.active_between(self.date_from, self.date_to)) > 0:
            raise OrderExistException
        super(AutoDateAddModel, self).save(*args, **kwargs)