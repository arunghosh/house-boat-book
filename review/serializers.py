from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('cleanliness', 'food', 'ambience', 'comment', 'date_created')