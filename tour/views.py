from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import get_object_or_404, redirect
from .models import Tour, TourDate, TourTime
from .forms import TourBookingForm

class TourListView(ListView):
    model = Tour
    template_name = "tour/tour_list.html"
    context_object_name = "tours"
    queryset = Tour.objects.filter(is_active=True)


class TourDetailView(DetailView, FormView):
    model = Tour
    template_name = "tour/tour_detail.html"
    context_object_name = "tour"
    form_class = TourBookingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dates"] = self.object.dates.all()
        context["images"] = self.object.images.all()
        return context

    def form_valid(self, form):
        tour = self.get_object()
        tour_date_id = self.request.POST.get("tour_date")
        tour_time_id = self.request.POST.get("tour_time")

        form.instance.tour = tour
        form.instance.tour_date = get_object_or_404(TourDate, id=tour_date_id)
        form.instance.tour_time = get_object_or_404(TourTime, id=tour_time_id)
        form.instance.user = self.request.user if self.request.user.is_authenticated else None
        form.save()
        return redirect("tours:booking_success")


from django.views.generic import TemplateView

class BookingSuccessView(TemplateView):
    template_name = "tour/booking_success.html"