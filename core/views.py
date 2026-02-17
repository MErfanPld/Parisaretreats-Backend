from django.shortcuts import render
from django.views.generic import TemplateView

from core.models import Slider
from tour.models import Tour

# Create your views here.


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(is_active=True).order_by('order')
        context['latest_tours'] = Tour.objects.filter(is_active=True).order_by('-created_at')[:3]
        return context