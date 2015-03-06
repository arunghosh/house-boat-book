from rest_framework import serializers
from .models import BaseUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        fields = ('name', 'email', 'phone')
