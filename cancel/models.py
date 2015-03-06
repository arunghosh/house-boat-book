from datetime import date, timedelta
from django.db import models
from util.modelfields import CurrencyField
from util.models import AutoDateAddModel
from boat.models import Boat
from order.models import Order

from .exception import InvalidPolicyException, AlreadyExistException


# class BaseCancelPolicyManager(models.QuerySet):
#
#     # def get_date(self, delta):
#     #     p_date = self.date + timedelta(days=-delta)
#     #     return p_date.strftime("%d %b %Y")
#
#     class Meta:
#         abstract = True

class CancelPolicyManager(models.QuerySet):

    def create_from_data(self, data, boat):
        p_id = data.get('id', 0)
        if p_id == 0:
            p = BoatCancelPolicy(boat=boat)
        else:
            p = BoatCancelPolicy.objects.get(pk=p_id)
        p.days = data['days']
        p.percent = data['percent']
        p.save()
        return p

    def add_to_order(self, order):
        for p in self.filter(is_active=True):
            OrderCancelPolicy.objects.create(days=p.days, percent=p.percent, order=order)

    def active(self):
        return self.filter(is_active=True)

    def common(self):
        return self.active().filter(boat=None)


class Cancel(AutoDateAddModel):
    order = models.OneToOneField(Order)
    amount_refund = CurrencyField()
    amount_cancel = CurrencyField()
    ip_address = models.GenericIPAddressField()


class BaseCancelPolicy(models.Model):
    days = models.PositiveSmallIntegerField()
    percent = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True


class OrderCancelPolicy(BaseCancelPolicy):
    order = models.ForeignKey(Order, related_name='cancel_policies')


class BoatCancelPolicy(BaseCancelPolicy):
    boat = models.ForeignKey(Boat, related_name='cancel_policies', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = CancelPolicyManager().as_manager()

    def save(self, *args, **kwargs):
        self.__validate()
        super(BaseCancelPolicy, self).save(*args, **kwargs)

    def __validate(self):
        if self.boat:
            policies = self.boat.cancel_policies.active()
        else:
            policies = BoatCancelPolicy.objects.common()

        invalid = [p for p in policies if (p.days > self.days and p.percent > self.percent) or (p.days < self.days and p.percent < self.percent)]
        if len(invalid) > 0:
            raise InvalidPolicyException

        duplicate = [p for p in policies if p.days == self.days and p.id != self.id]
        if len(duplicate) > 0:
            raise AlreadyExistException

    def __str__(self):
        return "{0} - {1}".format(self.boat.name if self.boat else "Common", self.days)