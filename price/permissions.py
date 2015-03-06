from rest_framework.permissions import BasePermission
from .models import Price


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in [o.user for o in obj.boat.company.owners.all()]
