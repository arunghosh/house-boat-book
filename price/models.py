from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _

from util.exception import PastDateException, CannotUpdateException
from util.models import AutoDateAddModel, BaseModel
from boat.models import Boat
from .exception import InvalidDateException


class SeasonPriceManager(models.QuerySet):

    def active(self):
        return self.filter(is_active=True)

    # def for_date(self, date):
    #     return PricePicker(self.active()).for_date(date)


class Price(BaseModel):
    base = models.PositiveIntegerField(verbose_name=_("Base Price"))
    adult = models.PositiveIntegerField(verbose_name=_("Extra cost per adult"))
    child = models.PositiveIntegerField(verbose_name=_("Extra cost per child"))

    def save(self, *args, **kwargs):
        if not self.is_new:
            raise CannotUpdateException
        super(BaseModel, self).save(*args, **kwargs)

    def __str__(self):
        return "B:%s,  A:%s,  C:%s" % (self.base, self.adult, self.child)


class SeasonPrice(AutoDateAddModel):
    price = models.ForeignKey(Price)
    boat = models.ForeignKey(Boat, related_name="season_prices")
    date_from = models.DateField()
    date_to = models.DateField()
    is_active = models.BooleanField(default=True)

    objects = SeasonPriceManager().as_manager()

    def save(self, *args, **kwargs):
        if self.date_to < self.date_from:
            raise InvalidDateException
        if self.date_from < date.today():
            raise PastDateException
        super(AutoDateAddModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.boat.name