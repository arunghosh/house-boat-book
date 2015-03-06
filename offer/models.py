from django.db import models
from django.utils.translation import ugettext_lazy as _

from util.modelfields import CurrencyField
from util.models import AutoDateAddModel
from boat.models import Boat


class OfferManager(models.Manager):

    def active(self, date):
        return self.get_queryset().filter(is_active=True)


class Offer(AutoDateAddModel):

    boat = models.ForeignKey(Boat, related_name='offers')
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    price = CurrencyField(verbose_name=_('Base Price'))
    text = models.CharField(max_length=128, verbose_name=_('Offer Tag Line'))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.boat.name

    class Meta:
        app_label="price"