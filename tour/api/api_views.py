# tour/api_views.py
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from ..models import TourBooking
from .serializers import TourBookingSerializer

class PaidTourBookingListAPIView(generics.ListAPIView):
    serializer_class = TourBookingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = TourBooking.objects.all().order_by('-id')
        tour_id = self.request.GET.get("tour_id")

        if tour_id:
            queryset = queryset.filter(tour_id=tour_id)

        return queryset