from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from django.db import transaction

from maintenance.models import Maintenance
from boat.models import Boat
from .models import Order
from util.views import get_json_response
from util.decorators import check_boat_access, check_order_access
from .serializers import OrderSerializers, OrderDetailsSerializers
from .exception import PastDateException, NotAvailableException, InvalidPriceException
from .parser import CreateRequestParser


def get_booked_boat_ids(request, year, month, day):
    p_date = date(int(year), int(month), int(day))
    ids = [o.boat.id for o in Order.objects.active_by_date(p_date)]
    ids += [m.boat.id for m in Maintenance.objects.get_for_date(p_date)]
    return get_json_response(list(set(ids)))


class BoatOrdersView(APIView):

    @check_boat_access
    def get(self, request):
        orders = request.boat.orders.all()
        slz = OrderSerializers(orders, many=True)
        return Response(slz.data)


class UpcomingBoatOrdersView(APIView):

    @check_boat_access
    def get(self, request, boat_id):
        orders = request.boat.orders.upcoming()
        slz = OrderSerializers(orders, many=True)
        return Response(slz.data)


class OrdersDetailsView(APIView):

    @check_order_access
    def get(self, request):
        slz = OrderDetailsSerializers(request.order)
        return Response(slz.data)


class OrderCreateView(APIView):

    @transaction.atomic
    def post(self, request):
        status = False
        msg = 'Booking successful'
        try:
            parser = CreateRequestParser(request)
            order = parser.create()
            order.confirm()
            status = True
        except PastDateException as ex:
            msg = str(ex)
        except NotAvailableException as ex:
            msg = str(ex)
        except InvalidPriceException as ex:
            msg = str(ex)
        # except Exception:
        #     msg = "Failed to create Order. Please contact help line."
        return Response({'status': status, 'msg': msg})

        # return Response({'status': status, 'msg':msg})