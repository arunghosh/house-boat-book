import json
from datetime import datetime, timedelta

from boat.models import Boat
from customer.models import Customer
from price.models import Price
from price import PricePicker
from util import get_ip_address
from util.parsers import get_date
from .exception import InvalidPriceException
from .models import Order


class CreateRequestParser:

    def __get_customer(self):
        email = self.__data['email'].lower().strip()
        cust_query = Customer.objects.filter(user__email=email)
        if len(cust_query) == 0:
            customer = Customer.objects.create_customer(
                email=email,
                name=self.__data['name'],
                phone=self.__data['phone'])
        else:
            customer = cust_query[0]
        return customer

    def __validate(self):
        picker = PricePicker(self.__boat)
        if self.__price.id != picker.for_date(self.__date).id:
            raise InvalidPriceException
        # Moved to order save
        # orders = self.__boat.orders.active_by_date(self.__date)
        # if len(orders) > 0:
        #     raise NotAvailableException
        # if self.__date <= datetime.now():
        #     raise PastDateException
    #   todo:
    #       check if the date time is valid and with in the rande

    def __init__(self, request):
        data = json.loads(request.body)
        self.__data = data
        self.__date = get_date(data['date_str'])
        # print self.__date
        self.__boat = Boat.objects.get(pk=self.__data['boat_id'])
        self.__customer = self.__get_customer()
        self.__price = Price.objects.get(pk=data['price_id'])
        self.__ip_address = get_ip_address(request)

    def create(self):
        self.__validate()
        data = self.__data
        order = Order.objects.create(
            customer=self.__customer,
            boat=self.__boat,
            date_in=self.__date,
            date_out=self.__date,
            price=self.__price,
            no_adult=data['no_adult'],
            no_child=data['no_child'],
            ip_address=self.__ip_address,
            cost_original=data['total'],
            cost_final=data['total'],
            commission=self.__boat.commission,
            source=Order.SRC_BOK,)
        self.__boat.cancel_policies.add_to_order(order)
        return order