from rest_framework.permissions import BasePermission
from .exception import AccessDeniedException

from boat.models import Boat

class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin

    def has_permission(self, request, view):
        return request.user.is_admin


# def check_owner_or_admin_(func):
#     def _inner(self, request, boat_id):
#         boat = Boat.objects.get(pk=boat_id)
#         check_owner_or_admin(boat, request.user)
#         request.boat = boat
#         return func(self, request)
#     return _inner


def check_owner_or_admin(boat, user):
    if user in [o.user for o in boat.company.owners.all()]:
        return
    if user.is_admin:
        return
    raise AccessDeniedException
