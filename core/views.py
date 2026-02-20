from django.shortcuts import render
from django.views.generic import TemplateView

from core.models import Slider
from tour.models import Tour
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Min
from datetime import timedelta

# Create your views here.

class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()
        one_week_ago = today - timedelta(days=7)

        context['sliders'] = Slider.objects.filter(is_active=True).order_by('order')

        context['latest_tours'] = (
            Tour.objects
            .filter(
                is_active=True,
                dates__end_date__gte=one_week_ago
            )
            .annotate(
                nearest_date=Min('dates__start_date')
            )
            .order_by('nearest_date')[:6]
        )

        return context
