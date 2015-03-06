import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from boat.models import Boat
from util.decorators import check_boat_access_from_post
from .models import Amenity


class UpdateBoatAmenityView(APIView):

    @check_boat_access_from_post('boat_id')
    def post(self, request):
        data = json.loads(request.body)
        amenity = Amenity.objects.get(pk=data['amenity_id'])
        if int(data['status']) == 1:
            request.boat.amenities.add(amenity)
        else:
            request.boat.amenities.remove(amenity)
        return Response({'status': True})