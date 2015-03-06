import json
from boat.models import Boat
from datetime import datetime
# from util.permissions import check_owner_or_admin
from util.parsers import get_date
from .models import Price, SeasonPrice


class BoatPriceUpdater:
    def __init__(self, request):
        data = json.loads(request.body)
        self.user = request.user
        self.data = data
        self.boat = request.boat

    def save(self):
        # check_owner_or_admin(self.boat, self.user)
        price = Price.objects.create(
            adult=self.data['adult'],
            child=self.data['child'],
            base=self.data['base'],
        )
        self.boat.price = price
        self.boat.save()
        return price


class SeasonPriceUpdater:
    def __init__(self, request):
        data = json.loads(request.body)
        self.user = request.user
        self.data = data
        self.boat = request.boat
        self.__get_old()
        self.__create_price()

    def __get_old(self):
        try:
            self.old_price = SeasonPrice.objects.get(pk=self.data['id'])
        except SeasonPrice.DoesNotExist:
            self.old_price = None

    def __create_price(self):
        self.price = Price.objects.create(
            adult=self.data['adult'],
            child=self.data['child'],
            base=self.data['base'],
        )

    def save(self):
        # check_owner_or_admin(self.boat, self.user)
        return self.__update()

    def __update(self):
        date_from = get_date(self.data['date_from'])
        date_to = get_date(self.data['date_to'])
        if self.old_price:
            season_price = self.old_price
            season_price.date_from = date_from
            season_price.date_to = date_to
            season_price.price = self.price
            season_price.save()
        else:
            season_price = SeasonPrice.objects.create(
                boat=self.boat,
                date_from=date_from,
                date_to=date_to,
                price=self.price,
            )
        return season_price