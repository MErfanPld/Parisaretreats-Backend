from django.urls import path
from .views import TourListView, TourDetailView, BookingSuccessView

app_name = "tours"

urlpatterns = [
    path("", TourListView.as_view(), name="tour_list"),
    path("<int:pk>/", TourDetailView.as_view(), name="tour_detail"),
    path("success/", BookingSuccessView.as_view(), name="booking_success"),
]
