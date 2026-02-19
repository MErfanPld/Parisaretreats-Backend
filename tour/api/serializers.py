# tour/serializers.py
from rest_framework import serializers
from ..models import TourBooking

class TourBookingSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = TourBooking
        fields = [
            "full_name",
            "phone_number",
            "tour",
            "tour_date",
            "tour_time",
            "number_of_people",
            "total_price",
        ]

    def get_total_price(self, obj):
        return obj.tour.price * obj.number_of_people
