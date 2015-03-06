from rest_framework import serializers
from django.conf import settings
from .models import Price, SeasonPrice


class PriceWithBoatIdSerializer(serializers.ModelSerializer):
    boat_id = serializers.RelatedField('boat.id')

    class Meta:
        model = Price
        fields = ('base', 'adult', 'child', 'id', 'boat_id',)


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ('base', 'adult', 'child', 'id',)


class SeasonPriceSerializer(serializers.ModelSerializer):
    boat_id = serializers.RelatedField('boat.id')
    adult = serializers.RelatedField('price.adult')
    child = serializers.RelatedField('price.child')
    base = serializers.RelatedField('price.base')
    date_from = serializers.DateField(format=settings.DATE_FORMAT)
    date_to = serializers.DateField(format=settings.DATE_FORMAT)

    class Meta:
        model = SeasonPrice
        fields = ('base', 'adult', 'child', 'boat_id', 'id', 'date_from', 'date_to')