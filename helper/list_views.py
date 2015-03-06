from django.shortcuts import render
from util.views import get_json_response

from amenity.models import Amenity
from amenity.serializers import AmenityMinSerializer
from boat.models import Boat


def amenities(request):
    amenities = Amenity.objects.all()
    slz = AmenityMinSerializer(amenities)
    return get_json_response(slz.data)


def ac_opts(request):
    opts = [{'name': b, 'id': a} for (a, b) in Boat.AC_CHOICES]
    return get_json_response(opts)