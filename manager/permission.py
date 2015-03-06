from rest_framework.permissions import BasePermission
from .models import Owner

class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in [o.user for o in obj.company.owners.all()]
        # return request.user.is_authenticated()

    def has_permission(self, request, view):
        # request.user in [o.user for o in company.owners.all()]
        return request.user.is_authenticated()