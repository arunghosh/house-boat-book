import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from order.models import Order
from .models import Review
from .serializers import ReviewSerializer


class BoatReviewsView(APIView):
    def get(self, request, boat_id):
        reviews = Review.objects.get_for_boat(boat_id)
        slz = ReviewSerializer(reviews)
        return Response(slz.data)


class AddReviewView(APIView):

    def get(self, request):
        # validate - travelled order
        return render(request, "review.html" , {})

    def post(self, request):
        data = json.loads(request.body)
        order = Order.objects.get(pk=data['order_id'])
        Review.objects.create(
            order=order,
            food=data['food'],
            cleanliness=data['cleanliness'],
            ambience=data['ambience'],
            comment=data['comment'],
        )
        return Response({'status': True})