from datetime import date
from threading import Lock

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from util.models import AutoDateAddModel
from util.modelfields import CurrencyField

from customer.models import Customer
from boat.models import Boat
from price.models import Price

from .signals import order_confirmed, order_cancelled
from .exception import NotAvailableException, PastDateException, CustomerCountException


order_create_lock = Lock()


class OrderManager(models.QuerySet):

    # def create_company_order(self, boat, date):
    #     order = Order.objects.create(
    #         customer=self.__customer,
    #         boat=self.__boat,
    #         date_in=date,
    #         date_out=date,
    #         # no_adult=0, no_child=0, cost_adult=0, cost_child=0, cost_base=0, cost_original=0, cost_final=0,
    #         source=Order.SRC_COMPANY,)

    def by_date(self, date):
        return self.filter(date_in=date)

    def by_status(self, status):
        return self.filter(order_status=status)

    def upcoming(self):
        return self.active().filter(date_in__gte=date.today())

    def active(self):
        return self.filter(order_status__in=Order.ACTIVE_STATUS_LST)

    def active_by_date(self, p_date):
        return self.active().filter(date_in=p_date)

    def active_between(self, date_from, date_to):
        return self.active().filter(date_in__range=(date_from, date_to))


class Order(AutoDateAddModel):
    STATUS_INITIAL = 0
    STATUS_CONFIRM = 10
    STATUS_TRAVEL = 15
    STATUS_CANCEL = 20
    STATUS_CLOSED = 30

    ACTIVE_STATUS_LST = (STATUS_CONFIRM, STATUS_TRAVEL,)

    STATUS_CHOICES = (
        (STATUS_INITIAL, _("Initial")),
        (STATUS_CONFIRM, _("Confirmed")),
        (STATUS_TRAVEL, _("Travelled")),
        (STATUS_CANCEL, _("Cancelled")),
    )

    SRC_BOK = 1
    SRC_COMPANY = 2

    SRC_CHOICES = (
        (SRC_BOK, "BoK"),
        (SRC_COMPANY, "Company")
    )

    customer = models.ForeignKey(Customer, related_name="orders")
    boat = models.ForeignKey(Boat, related_name="orders")
    price = models.ForeignKey(Price, related_name="orders", null=True)

    no_adult = models.PositiveSmallIntegerField(default=0)
    no_child = models.PositiveSmallIntegerField(default=0)
    is_veg = models.BooleanField(_("Is vegetarian cuisine"), default=False)
    require_pick = models.BooleanField(_("Require pick and drop"), default=False)
    agreed_terms = models.BooleanField(default=False)
    date_in = models.DateField()
    date_out = models.DateField()
    date_confirm = models.DateField(null=True, blank=True)

    cost_original = CurrencyField(default=0)
    cost_final = CurrencyField(default=0)
    commission = models.SmallIntegerField(default=10)
    order_status = models.SmallIntegerField(default=STATUS_INITIAL, choices=STATUS_CHOICES)

    source = models.SmallIntegerField(default=SRC_BOK)
    is_active = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField()

    objects = OrderManager().as_manager()

    def confirm(self):
        self.date_confirm = timezone.now()
        self.order_status = Order.STATUS_CONFIRM
        self.save()
        self.add_comment("order confirmed")
        order_confirmed.send(self)

    def cancel_order(self):
        self.order_status = Order.STATUS_CANCEL
        self.save()
        self.add_comment("order cancelled")
        order_cancelled.send(self)

    def add_comment(self, text):
        OrderComments.objects.create(order=self, text=text)

    def save(self, *args, **kwargs):
        with order_create_lock:
            self.__validate()
            super(AutoDateAddModel, self).save(*args, **kwargs)

    def __validate(self):
        orders = self.boat.orders.active_by_date(self.date_in)
        if len([o for o in orders if o != self]) > 0:
            raise NotAvailableException
        if self.is_new and self.date_in <= date.today():
            raise PastDateException
        if self.no_adult > self.boat.max_adult or self.no_child > self.boat.max_child:
            raise CustomerCountException


class OrderComments(models.Model):
    order = models.ForeignKey(Order, related_name="comments")
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=256)