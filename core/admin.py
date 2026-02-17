from django.contrib import admin
from .models import Slider

# Register your models here.

admin.site.site_header = "Dashboard Parisaretreats"
admin.site.site_title = "Dashboard"
admin.site.index_title = "Welcome"

# -------------------------------
# Slider Admin
# -------------------------------
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title",)
    ordering = ("order",)