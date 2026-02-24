# tour/serializers.py
from rest_framework import serializers
from ..models import TourBooking

class TourBookingSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    tour_id = serializers.IntegerField(source="tour.id")
    tour_title = serializers.CharField(source="tour.title")

    class Meta:
        model = TourBooking
        fields = [
            "id",
            "full_name",
            "phone_number",
            "tour_title",
            "tour_id",   # 👈 اضافه شد
            "tour_date",
            "tour_time",
            "number_of_people",
            "total_price",
            "payment_receipt",
        ]

    def get_total_price(self, obj):
        return obj.tour.price * obj.number_of_people
