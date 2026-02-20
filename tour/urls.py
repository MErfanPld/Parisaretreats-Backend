from django.urls import path

from tour.api.api_views import PaidTourBookingListAPIView
from .views import TourListView, TourDetailView, BookingSuccessView,TourBookingExtraView

app_name = "tours"

urlpatterns = [
    path("", TourListView.as_view(), name="tour_list"),
    path("<int:pk>/", TourDetailView.as_view(), name="tour_detail"),
    path(
        "booking/<int:pk>/extra/",
        TourBookingExtraView.as_view(),
        name="booking_extra"
    ),
    path("success/", BookingSuccessView.as_view(), name="booking_success"),
    path('api/paid_bookings/', PaidTourBookingListAPIView.as_view(), name='paid-bookings'),
]
