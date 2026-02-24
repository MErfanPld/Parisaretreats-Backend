from django.urls import path

from tour.api.api_views import PaidTourBookingListAPIView
from .views import ManualPaymentView, TourListView, TourDetailView, BookingSuccessView,TourBookingExtraView

app_name = "tours"

urlpatterns = [
    path("", TourListView.as_view(), name="tour_list"),
    path("<int:pk>/", TourDetailView.as_view(), name="tour_detail"),
    path(
        "booking/extra/",
        TourBookingExtraView.as_view(),
        name="booking_extra"
    ),
    path("success/", BookingSuccessView.as_view(), name="booking_success"),
    path("payment/", ManualPaymentView.as_view(), name="manual_payment"),
    path('api/paid_bookings/', PaidTourBookingListAPIView.as_view(), name='paid-bookings'),
]
