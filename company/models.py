from django.db import models
from util.models import AutoDateAddModel
from account.models import BaseUser


class Company(AutoDateAddModel):
    name = models.CharField(max_length=128)
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @property
    def orders(self):
        orders = [o for b in self.boats.all() for o in b.orders.all()]
        return orders

    class Meta:
        app_label = "company"


class Owner(AutoDateAddModel):
    user = models.ForeignKey(BaseUser)
    company = models.ForeignKey(Company, related_name="owners")

    def __unicode__(self):
        return self.user.name

    class Meta:
        app_label = "company"


# @receiver(order_cancelled)
# def __on_order_cancel(sender, **kwargs):
#     OrderMail(sender).send_order_cancel()
#     sender.add_comment("cancel mail send to customer")
#
# @receiver(order_confirmed)
# def __on_order_confirm(sender, **kwargs):
#     OrderMail(sender).send_order_confirm()
#     sender.add_comment("confirm mail send customer")