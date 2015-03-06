from datetime import date, timedelta
import json
from django.db import transaction
from rest_framework.response import Response
from cancel.serializers import OrderCancelPolicySerializer
from order.models import Order
from order.serializers import OrderSerializers
from util import get_ip_address
from .models import Cancel
from .exception import AlreadyCancelledException, InvalidOrderReqException


class CancelHelper:

    STEP_DETAIL_REQ = 10
    STEP_CANCEL_REQ = 20
    STEP_CANCELED = 90

    def __init__(self, request):

        # plaintext = get_template('emails/base.txt')
        # htmly = get_template('emails/base.html')
        # d = Context({'user_name': "arun" })
        # subject, from_email, to = 'hello', 'arunghosh@gmail.com', 'arunghosh@gmail.com'
        # text_content = plaintext.render(d)
        # html_content = htmly.render(d)
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        self.request = request
        self.data = json.loads(request.body)
        self.step = self.data.get('step', CancelHelper.STEP_DETAIL_REQ)
        self.__validate_request()
        self.policy = self.__get_cancel_policy()
        self.amount_cancel = self.order.cost_final * self.policy.percent / 100
        self.amount_refund = self.order.cost_final - self.amount_cancel

    def __validate_request(self):
        try:
            order = Order.objects.get(pk=self.data['order_id'])
        except Order.DoesNotExist:
            raise InvalidOrderReqException
        if order.customer.user.email != self.data['user_email']:
            raise InvalidOrderReqException
        if order.order_status == Order.STATUS_CANCEL:
            raise AlreadyCancelledException
        if order.order_status != order.STATUS_CONFIRM:
            raise InvalidOrderReqException
        self.order = order

    def process_request(self):
        if self.step == CancelHelper.STEP_CANCEL_REQ:
            return self.__cancel_order()
        elif self.step == CancelHelper.STEP_DETAIL_REQ:
            return self.__get_details()
        else:
            # invalid
            pass

    def __get_details(self):
        order_slz = OrderSerializers(self.order)
        policies = PolicyFormatter(list(self.order.cancel_policies.all()), self.order.date_in).policies
        policy_slz = OrderCancelPolicySerializer(policies, many=True)
        return {
            'status': True,
            'step': CancelHelper.STEP_CANCEL_REQ,
            'order': order_slz.data,
            'policies': policy_slz.data,
            'cancel_amount': self.amount_cancel,
            'refund_amount': self.amount_refund,
            'policy_id': self.policy.id}


    @transaction.atomic
    def __cancel_order(self):
        Cancel.objects.create(
            order=self.order,
            ip_address=get_ip_address(self.request),
            amount_cancel=self.amount_cancel,
            amount_refund=self.amount_refund)
        self.order.cancel_order()
        return {
            'status': True,
            'is_cancelled': True,
            'step': CancelHelper.STEP_CANCELED}

    def __get_cancel_policy(self):
        delta = (self.order.date_in - date.today()).days
        policies = self.order.cancel_policies.all()
        if policies[0].days > delta:
            return policies[0]

        if policies[1].days < delta:
            return policies[1]

        for index, p in enumerate(policies[1:-1]):
            if p.days - policies[index].days == 1 and delta == p.days:
                return p
            elif p.days > delta >= policies[index].days:
                return p


class PolicyFormatter:

    def __init__(self, policies, order_date):
        self.date = order_date
        policies[0].text = "On or after {0}".format(self.get_date(policies[0].days))
        policies[-1].text = "On or before {0}".format(self.get_date(policies[-1].days))
        for index, p in enumerate(policies[1:-1]):
            if p.days - policies[index].days == 1:
                p.text = "On {0}".format(self.get_date(p.days))
            else:
                p.text = "Between {0} & {1}".format(self.get_date(policies[index].days), self.get_date(p.days))
        self.policies = policies

    def get_date(self, delta):
        p_date = self.date + timedelta(days=-delta)
        return p_date.strftime("%d %b %Y")