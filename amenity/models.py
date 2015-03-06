from django.db import models
from django.utils.translation import ugettext_lazy as _


class AmenityManager(models.Manager):

    def searchable(self):
        return self.get_queryset().filter(searchable=True)


class Amenity(models.Model):
    name = models.CharField(max_length=32, unique=True)
    specification = models.CharField(max_length=32, null=True, blank=True)
    searchable = models.BooleanField(default=True, verbose_name=_("Is Searchable"))
    deleted = models.BooleanField(default=False)

    objects = AmenityManager()

    def __unicode__(self):
        return self.name #+ str(len(self.hall_set.all()))

    class Meta:
        app_label = "boat"
        verbose_name = _('amenity')
        verbose_name_plural = _('amenities')