from django.contrib import admin
from .models import BaseUser

class UserAdmin(admin.ModelAdmin):

    def save_model(self, request, user, form, change):
        if user.password:
            user.set_password(user.password)
        user.save()

    class Meta:
        model = BaseUser


admin.site.register(BaseUser, UserAdmin)
