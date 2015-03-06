from django.contrib import admin
from .models import BoatCancelPolicy

@admin.register(BoatCancelPolicy)
class PolicyAdmin(admin.ModelAdmin):
    pass