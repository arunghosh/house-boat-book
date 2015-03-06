from datetime import date, timedelta
import calendar
from dateutil import rrule
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from boat.models import Boat
from .serializers import PriceWithBoatIdSerializer, SeasonPriceSerializer, PriceSerializer
from . import PricePicker, MonthPriceHelper
from .updater import SeasonPriceUpdater, BoatPriceUpdater
from util.decorators import check_boat_access, check_boat_access_from_post


class DatePricesView(APIView):

    def get(self, request, year, month, day):
        p_date = date(int(year), int(month), int(day))
        prices = [PricePicker(b).for_date(p_date) for b in Boat.objects.active()]
        slz = PriceWithBoatIdSerializer([p for p in prices if p], many=True)
        return Response(slz.data)


class BoatDatePricesView(APIView):

    @check_boat_access
    def get(self, request, year, month, day):
        p_date = date(int(year), int(month), int(day))
        price = PricePicker(request.boat).for_date(p_date)
        slz = PriceWithBoatIdSerializer(price)
        return Response(slz.data)


class BoatPricesView(APIView):

    @check_boat_access
    def get(self, request):
        boat = request.boat
        season_prices = boat.season_prices.active()
        season_slz = SeasonPriceSerializer(season_prices, many=True)
        price = boat.price
        slz = PriceSerializer(price)
        return Response({
            'season': season_slz.data,
            'base': slz.data})


class MonthView(APIView):

    @check_boat_access
    def get(self, request, month, year):
        helper = MonthPriceHelper(request, month, year)
        return Response({
            'data': helper.get_prices(),
            'price': request.boat.price.base
        })


class UpdateBoatPriceView(APIView):

    @transaction.atomic
    @check_boat_access_from_post('boat_id')
    def post(self, request):
        try:
            updater = BoatPriceUpdater(request)
            price = updater.save()
        except Exception as ex:
            return Response({
                'status': False,
                'msg': str(ex)})
        return Response({
            'status': True,
            'data': PriceSerializer(price).data})


class UpdateSeasonPriceView(APIView):

    @transaction.atomic
    @check_boat_access_from_post('boat_id')
    def post(self, request):
        try:
            updater = SeasonPriceUpdater(request)
            price = updater.save()
        except Exception as ex:
            return Response({
                'status': False,
                'msg': str(ex)})
        return Response({
            'status': True,
            'data': SeasonPriceSerializer(price).data})