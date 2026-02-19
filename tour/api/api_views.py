# tour/api_views.py
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from ..models import TourBooking
from .serializers import TourBookingSerializer

class PaidTourBookingListAPIView(generics.ListAPIView):
    queryset = TourBooking.objects.filter(is_paid=True).order_by('-id')
    serializer_class = TourBookingSerializer
    permission_classes = [AllowAny]
