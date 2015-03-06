import json
from django.shortcuts import render
from datetime import  date, timedelta
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response

from boat.models import Boat
from util.permissions import IsAdmin
from .models import BoatCancelPolicy
from .forms import OrderCancelForm
from .serializers import BoatCancelPolicySerializer, CancelPolicySerializer
from . import PolicyFormatter, CancelHelper

import pdb
# class CancelPolicyViewSet(viewsets.ModelViewSet):
#     serializer_class = CancelPolicySerializer
#     queryset = Policy.objects.all()
from util.decorators import check_boat_access


class OrderCancelView(APIView):

    def get(self, request):
        form = OrderCancelForm()
        return render(request, 'order/cancel.html', {'form': form})

    @transaction.atomic
    def post(self, request):
        try:
            helper = CancelHelper(request)
            return Response(helper.process_request())
        except Exception as ex:
            return Response({'status': False, 'msg': str(ex)})


class BoatDatePoliciesView(APIView):

    def __init__(self, *args, **kwargs):
        super(BoatDatePoliciesView, self).__init__(**kwargs)
        self.date = None
        self.boat_id = None

    def get(self, request, boat_id, year, month, day):
        p_date = date(int(year), int(month), int(day))
        self.boat_id = boat_id
        policies = PolicyFormatter(self.__policies, p_date).policies
        slz = BoatCancelPolicySerializer(policies, many=True)
        return Response(slz.data)

    @property
    def __policies(self):
        policies = list(Boat.objects.get(pk=self.boat_id).cancel_policies.active())
        if len(policies) == 0:
            policies = list(BoatCancelPolicy.objects.common())
        policies.sort(key=lambda x: x.days)
        return policies


class CommonCancelPolicyView(APIView):

    permission_classes = (IsAdmin, )

    def get(self, request):
        policies = BoatCancelPolicy.objects.common()
        return Response(CancelPolicySerializer(policies, many=True).data)

    def post(self, request):
        data = json.loads(request.body)
        try:
            p = BoatCancelPolicy.objects.create_from_data(data, None)
            return Response({
                'status': True,
                'data': CancelPolicySerializer(p).data})
        except Exception as ex:
            return Response({
                'status': False,
                'msg': str(ex)})


class BoatCancelPolicyView(APIView):

    @check_boat_access
    def get(self, request):
        policies = request.boat.cancel_policies.all()
        return Response(CancelPolicySerializer(policies, many=True).data)

    @check_boat_access
    def post(self, request, boat_id):
        data = json.loads(request.body)
        try:
            p = BoatCancelPolicy.objects.create_from_data(data, request.boat)
            return Response({
                'status': True,
                'data': CancelPolicySerializer(p).data})
        except Exception as ex:
            return Response({
                'status': False,
                'msg': str(ex)})