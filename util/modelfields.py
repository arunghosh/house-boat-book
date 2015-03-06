from django.db import models
from decimal import Decimal


class CurrencyField(models.DecimalField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(CurrencyField, self).__init__(**kwargs)
        self.decimal_places = 2
        self.max_digits = 10

    def to_python(self, value):
        try:
           return super(CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
        except AttributeError:
           return None