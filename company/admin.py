from django.contrib import admin
from .models import Company, Owner


class CompanyAdmin(admin.ModelAdmin):

    class Meta:
        model = Company


class OwnerAdmin(admin.ModelAdmin):

    class Meta:
        model = Owner


admin.site.register(Company, CompanyAdmin)
admin.site.register(Owner, OwnerAdmin)