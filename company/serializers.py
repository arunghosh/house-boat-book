from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Company, Owner


class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Owner
        fields = ('user', )


class CompanySerializer(serializers.ModelSerializer):
    no_boats = serializers.SerializerMethodField('get_no_boats')
    # no_orders = serializers.SerializerMethodField('get_no_orders')

    class Meta:
        model = Company
        fields = ('name', 'id', 'no_boats',)# 'no_orders')

    def get_no_boats(self, obj):
        return len(obj.boats.all())