from django import forms

from order.models import Order


class OrderCancelForm(forms.Form):

    order_id = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        self.custom_errors = []
        self.user = None
        self.status = False
        self.order = None
        super(OrderCancelForm, self).__init__(*args, **kwargs)

    def cancel_order(self):

        if self.is_valid():
            try:
                self.order = Order.objects.get(pk=self.cleaned_data['order_id'])
                if self.order.customer.user.email == self.cleaned_data['email'].strip().lower():
                    self.status = True
                else:
                    pass
            except Order.DoesNotExist:
                pass
        else:
            pass
        if not self.status:
            self.custom_errors.append("Invalid order ID or email")
