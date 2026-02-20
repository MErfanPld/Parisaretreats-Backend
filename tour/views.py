from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from .models import Tour, TourBooking, TourDate, TourTime
from .forms import TourBookingExtraForm, TourBookingForm

class TourListView(ListView):
    model = Tour
    template_name = "tour/tour_list.html"
    context_object_name = "tours"
    queryset = Tour.objects.filter(is_active=True)



from django.shortcuts import redirect, get_object_or_404

class TourDetailView(DetailView):
    model = Tour
    template_name = "tour/tour_detail.html"
    context_object_name = "tour"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dates"] = self.object.dates.all()
        context["images"] = self.object.images.all()
        context["form"] = TourBookingForm()  # اضافه کردن فرم
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # مهم: self.object باید ست شود

        # اگر کاربر لاگین نکرده بود، مستقیم به صفحه لاگین بره
        if not request.user.is_authenticated:
            # می‌تونیم با next بفرستیم بعد از لاگین دوباره همین صفحه بیاد
            return redirect(f"/accounts/login/?next={request.path}")

        form = TourBookingForm(request.POST)
        tour_date_id = request.POST.get("tour_date")
        tour_time_id = request.POST.get("tour_time")

        if form.is_valid():
            tour_date = get_object_or_404(TourDate, id=tour_date_id)
            tour_time = get_object_or_404(TourTime, id=tour_time_id)

            requested_people = form.cleaned_data.get("number_of_people", 1)
            remaining = self.object.remaining_capacity(tour_date)

            if requested_people > remaining:
                form.add_error(
                    "number_of_people",
                    f"The remaining capacity for this tour for this date is {remaining} people."
                )
                context = self.get_context_data()
                context["form"] = form
                return self.render_to_response(context)

            # ذخیره رزرو
            form.instance.tour = self.object
            form.instance.tour_date = tour_date
            form.instance.tour_time = tour_time
            form.instance.user = request.user
            booking = form.save()
            return redirect("tours:booking_extra", pk=booking.pk)
        else:
            context = self.get_context_data()
            context["form"] = form
            return self.render_to_response(context)



class TourBookingExtraView(LoginRequiredMixin, UpdateView):
    model = TourBooking
    form_class = TourBookingExtraForm
    template_name = "tour/booking_extra.html"
    context_object_name = "booking"

    def get_queryset(self):
        # فقط رزروهای کاربر لاگین کرده
        return TourBooking.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("tours:booking_success")


from django.views.generic import TemplateView

class BookingSuccessView(TemplateView):
    template_name = "tour/booking_success.html"