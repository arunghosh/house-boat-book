from django.db import models

from django.utils.translation import ugettext_lazy as _
from util.models import AutoDateAddModel
from util.modelfields import CurrencyField
from company.models import Company
from amenity.models import Amenity


class BoatManager(models.QuerySet):

    def active(self):
        return self.filter(is_bok=True)


class Boat(AutoDateAddModel):

    AC_FULL = 1
    AC_PARTIAL = 2
    AC_NON = 3
    AC_CHOICES = (
        (AC_FULL, 'Full Time AC'),
        (AC_PARTIAL, 'Partial AC'),
        (AC_NON, 'Non AC'),
    )

    FTR_LX = 1
    FTR_PR = 2
    FTR_DX = 3
    FTR_CHOICES = (
        (FTR_LX, 'Luxury'),
        (FTR_PR, 'Premium'),
        (FTR_DX, 'Deluxe'),
    )

    name = models.CharField(max_length=64, verbose_name=_("Boat Name"))
    company = models.ForeignKey(Company, related_name="boats")
    no_room = models.PositiveSmallIntegerField(default=2, verbose_name=_("No of rooms"))
    type = models.SmallIntegerField(choices=FTR_CHOICES, default=1)
    ac_type = models.SmallIntegerField(choices=AC_CHOICES, verbose_name=_("A/C types"))
    no_adult = models.PositiveIntegerField(default=2, verbose_name=_("Number of adults"))
    max_adult = models.PositiveIntegerField(default=4, verbose_name=_("Max number adults"))
    max_child = models.PositiveIntegerField(default=4, verbose_name=_("Max allowed children"))
    price = models.ForeignKey("price.Price", related_name="boats")
    is_bok = models.BooleanField(default=True, verbose_name=_("Is available to BoK"))
    commission = models.SmallIntegerField(default=10)

    # review_count = models.PositiveSmallIntegerField(default=0)
    # review_avg = models.DecimalField(default=0, dec)

    amenities = models.ManyToManyField(Amenity, null=True, blank=True)

    objects = BoatManager().as_manager()

    @property
    def review_avg(self):
        reviews = [r for o in self.orders.all() for r in o.reviews.all()]
        return sum([r.avg for r in reviews]) / len(reviews) if len(reviews) > 0 else 0

    @property
    def review_cnt(self):
        reviews = [r for o in self.orders.all() for r in o.reviews.all()]
        return len(reviews)


    @property
    def company_name(self):
        return self.company.name

    def __str__(self):
        return self.name


class Image(AutoDateAddModel):
    boat = models.ForeignKey(Boat, related_name="images")
    image = models.ImageField(upload_to="boat_images")
    description = models.CharField(max_length=256)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.boat.name

    #
    # STAT_ACTIVE = 0
    # STAT_MAINTENANCE = 1
    # STAT_REMOVED = 2
    # STAT_CHOICES = (
    #     (STAT_ACTIVE, 'Active'),
    #     (STAT_MAINTENANCE, 'Maintenance'),
    #     (STAT_REMOVED, 'Removed'),
    # )