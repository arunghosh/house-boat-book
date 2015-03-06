from rest_framework import serializers
from .models import Boat, Image


class BoatSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Boat
        fields = ('url', 'name', 'id', )


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.RelatedField("image.url")

    class Meta:
        model = Image
        fields = ('url', 'description',)


class BoatDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    amenities = serializers.RelatedField(many=True)
    ac_type = serializers.SerializerMethodField('get_ac_type')
    type = serializers.SerializerMethodField('get_type')
    company = serializers.RelatedField("company.name")
    review_avg = serializers.DecimalField()
    review_cnt = serializers.IntegerField()

    class Meta:
        model = Boat
        fields = ('name', 'id', 'no_room',
                  'amenities', 'ac_type',
                  'company', 'no_adult', 'no_adult',
                  'max_adult', 'max_child', 'review_avg', 'is_bok',
                  'images', 'type', 'review_cnt',)

    def get_ac_type(self, obj):
        return [b for (a, b) in Boat.AC_CHOICES if a == obj.ac_type][0]

    def get_type(self, obj):
        return [b for (a, b) in Boat.FTR_CHOICES if a == obj.type][0]
