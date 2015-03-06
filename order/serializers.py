from rest_framework import serializers
from price.serializers import PriceSerializer
from .models import Order

FIELDS = ('is_veg', 'commission', 'date_in', 'status', 'boat_name',
          'no_child', 'no_adult', 'source', 'date_confirm', 'cost_final', 'id' )


class OrderSerializers(serializers.ModelSerializer):
    boat_name = serializers.RelatedField('boat.name')
    status = serializers.SerializerMethodField('get_status')
    source = serializers.SerializerMethodField('get_source')

    def get_status(self, obj):
        return [b for (a, b) in Order.STATUS_CHOICES if a == obj.order_status][0]

    def get_source(self, obj):
        return [b for (a, b) in Order.SRC_CHOICES if a == obj.source][0]

    class Meta:
        model = Order
        fields = FIELDS


class OrderDetailsSerializers(OrderSerializers):
    price_base = serializers.RelatedField('price.base')

    class Meta:
        model = Order
        fields = FIELDS + ('price_base',)