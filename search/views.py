from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .filters import BoatFinder
from account.models import BaseUser



# class SearchView(APIView):
#
def home(request):
    # BaseUser.objects.create_superuser("abcd@gmail.com", "abcd1234", "Abcd")
    return render(request, 'index.html', {})


class BoatIdsView(APIView):

    def post(self, request):
        finder = BoatFinder(request)
        boats = finder.get_boats()
        ids = [b.id for b in boats]
        return Response(ids)