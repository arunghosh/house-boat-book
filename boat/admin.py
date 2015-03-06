from django.contrib import admin
from .models import Boat, Image


@admin.register(Boat)
class BoatAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'no_room', 'is_bok')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass