from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework import viewsets, generics
from rest_framework.response import Response

from util.permissions import IsAdmin
from order.serializers import OrderSerializers, Order

from .forms import LoginForm
from .menus import MainMenu
from company.models import Company, Owner


def logout_user(request):
    logout(request)
    return redirect("/manage/")


class MenuView(APIView):

    def get(self, request):
        return Response(MainMenu.get(request.user))


class HomeView(View):

    def get(self, request):
        if request.user.is_authenticated():
            return self.home_view(request)
        form = LoginForm()
        return render(request, "manager/login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        form.authenticate(request)
        if request.user.is_authenticated():
            return self.home_view(request)
        return render(request, "manager/login.html", {'form': form})

    def home_view(self, request):
        if request.user.is_bok:
            return render(request, "manager/bok.html", {})
        else:
            return redirect("/company/")


# class BoatsAPI(generics.ListAPIView):
#     serializer_class = BoatDetailSerializer
#     # permission_classes = (IsOwner, )
#     queryset = Boat.objects.all()
#
#     def get_queryset(self):
#         if self.request.user.is_admin:
#             boats = Boat.objects.all()
#         else:
#             boats = Owner.objects.get(user=self.request.user).company.boats.all()
#         return boats
#
#
class OrderAPI(generics.ListAPIView):
    serializer_class = OrderSerializers
    permission_classes = (IsAdmin, )
    queryset = Order.objects.all()

    def get_queryset(self):
        orders = list(Order.objects.upcoming())
        orders.sort(key=lambda x: x.date_in)
        return orders