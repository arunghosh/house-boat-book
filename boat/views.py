import json
from django.shortcuts import render
from boat.models import Boat
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BoatDetailSerializer
from util.decorators import check_boat_access_from_post


class ActiveBoatsAPI(generics.ListAPIView):
    serializer_class = BoatDetailSerializer
    queryset = Boat.objects.active()


def boat_detail(request):
    return render(request, "manager/boat.html", {})


class AllBoatsViewSet(viewsets.ModelViewSet):
    serializer_class = BoatDetailSerializer
    queryset = Boat.objects.all()


class BoatUpdateView(APIView):

    @check_boat_access_from_post('id')
    def post(self, request):
        data = json.loads(request.body)
        boat = request.boat
        boat.max_adult = data['max_adult']
        boat.max_child = data['max_child']
        boat.name = data['name']
        boat.ac_type = [a for (a, b) in Boat.AC_CHOICES if b == data['ac_type']][0]
        boat.no_room = data['no_room']
        boat.save()
        return Response(BoatDetailSerializer(boat).data)