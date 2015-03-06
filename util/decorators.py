import json
from boat.models import Boat
from order.models import Order
from util.permissions import check_owner_or_admin

def check_boat_access_from_post(key):
    def _outer(func):
        def _inner(self, request, *args, **kwargs):
            data = json.loads(request.body)
            boat = Boat.objects.get(pk=data[key])
            check_owner_or_admin(boat, request.user)
            request.boat = boat
            return func(self, request, *args, **kwargs)
        return _inner
    return _outer


def check_boat_access(func):
    def _inner(self, request, boat_id, *args, **kwargs):
        boat = Boat.objects.get(pk=boat_id)
        check_owner_or_admin(boat, request.user)
        request.boat = boat
        return func(self, request, *args, **kwargs)
    return _inner


def check_order_access(func):
    def _inner(self, request, order_id, *args, **kwargs):
        order = Order.objects.get(pk=order_id)
        check_owner_or_admin(order.boat, request.user)
        request.boat = order.boat
        request.order = order
        return func(self, request, *args, **kwargs)
    return _inner
