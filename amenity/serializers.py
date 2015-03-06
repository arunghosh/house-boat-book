from rest_framework import serializers
from .models import Amenity

class AmenityMinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = ('id', 'name',)
