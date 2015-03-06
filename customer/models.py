from django.db import models
from django.dispatch import receiver
from util.models import AutoDateAddModel
from account.models import BaseUser
from order.signals import order_cancelled, order_confirmed
from order.notifications import MailNotification
from .exception import UserNotCustomerException


class CustomerManager(models.Manager):

    def create_customer(self, name, email, phone):
        user = BaseUser.objects.create_customer(
            name=name,
            email=email,
            phone=phone)
        customer = Customer.objects.create(user=user)
        return customer


class Customer(AutoDateAddModel):
    user = models.OneToOneField(BaseUser)
    objects = CustomerManager()

    def save(self, *args, **kwargs):
        if not self.user.is_customer:
            raise UserNotCustomerException
        super(AutoDateAddModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.name

    class Meta:
        app_label = 'order'


@receiver(order_cancelled)
def __on_order_cancel(sender, **kwargs):
    MailNotification(sender).send_order_cancel()
    sender.add_comment("cancel mail send to customer")


@receiver(order_confirmed)
def __on_order_confirm(sender, **kwargs):
    MailNotification(sender).send_order_confirm()
    sender.add_comment("confirm mail send customer")