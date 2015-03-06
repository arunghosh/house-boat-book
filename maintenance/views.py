import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from util.parsers import get_date
from .models import Maintenance
from .serializers import MaintenanceSerializer
from util.decorators import check_boat_access


class MaintenanceView(APIView):
    def get(self, request, boat_id):
        blocks = Maintenance.objects.get_for_boat_id(boat_id)
        slz = MaintenanceSerializer(blocks, many=True)
        return Response(slz.data)

    @check_boat_access
    def post(self, request):
        data = json.loads(request.body)
        try:
            mt = Maintenance.objects.create(
                date_from=get_date(data['date_from']),
                date_to=get_date(data['date_to']),
                boat=request.boat
            )
            return Response({
                'status': True,
                'data': MaintenanceSerializer(mt).data})
        except Exception as ex:
            return Response({
                'status': False,
                'msg': str(ex)})
    # def delete(self, request, boat_id):
    #     data = json.loads(request.body)
    #     mt = Maintenance.objects.remove(p)
    #     return Response(MaintenanceSerializer(mt).data)

