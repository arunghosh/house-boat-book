from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

from util.permissions import IsAdmin
from boat.models import Boat
from boat.serializers import BoatSerializer, BoatDetailSerializer
from order.serializers import OrderSerializers, Order
from .models import Company, Owner
from .serializers import CompanySerializer, OwnerSerializer


def home(request):
    return render(request, "manager/company.html")


class CompanyDetailsView(APIView):

    def get(self, request):
        company = Owner.objects.filter(user=request.user)[0].company
        return Response(CompanySerializer(company).data)


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin, )
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class BoatsAPI(APIView):

    def get(self, request, company_id):
        boats = Boat.objects.filter(company__id=company_id)
        return Response(BoatDetailSerializer(boats, many=True).data)


class OrdersAPI(APIView):

    def get(self, request, company_id):
        orders = Order.objects.filter(boat__company__id=company_id)
        return Response(OrderSerializers(orders, many=True).data)


class UpcomingOrdersAPI(APIView):

    def get(self, request, company_id):
        orders = Order.objects.upcoming().filter(boat__company__id=company_id)
        return Response(OrderSerializers(orders, many=True).data)


class OwnersAPI(APIView):

    def get(self, request, company_id):
        owners = Owner.objects.filter(company__id=company_id)
        return Response(OwnerSerializer(owners, many=True).data)
