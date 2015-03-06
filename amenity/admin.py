from django.contrib import admin
from .models import Amenity


class AmenityAdmin(admin.ModelAdmin):
    class Meta:
        model = Amenity


admin.site.register(Amenity, AmenityAdmin)