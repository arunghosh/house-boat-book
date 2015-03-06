from rest_framework import serializers
from .models import BoatCancelPolicy, OrderCancelPolicy


class BoatCancelPolicySerializer(serializers.ModelSerializer):

    boat_id = serializers.RelatedField('boat.id')
    text = serializers.CharField()

    class Meta:
        model = BoatCancelPolicy
        fields = ('days', 'percent', 'boat_id', 'text',)


class OrderCancelPolicySerializer(serializers.ModelSerializer):

    text = serializers.CharField()

    class Meta:
        model = BoatCancelPolicy
        fields = ('days' , 'percent', 'text', 'id',)


class CancelPolicySerializer(serializers.ModelSerializer):

    text = serializers.CharField()

    class Meta:
        model = BoatCancelPolicy
        fields = ('days' , 'percent', 'id',)