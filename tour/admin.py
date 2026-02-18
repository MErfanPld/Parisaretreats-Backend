from django.contrib import admin
from django.forms import ValidationError
from .models import Tour, TourDate, TourFeature, TourTime, TourImage, TourBooking

# Inline برای نمایش تصاویر در تور
class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1


# Inline برای نمایش تاریخ‌ها در تور
class TourDateInline(admin.TabularInline):
    model = TourDate
    extra = 1


# Inline برای نمایش ساعت‌ها در تاریخ
class TourTimeInline(admin.TabularInline):
    model = TourTime
    extra = 1


@admin.register(TourFeature)
class TourFeatureAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("title", "price", 'image',"is_active", "created_at")
    inlines = [TourDateInline, TourImageInline]
    filter_horizontal = ("features",)
    
    
@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ("tour", "start_date", "end_date")
    inlines = [TourTimeInline]


@admin.register(TourTime)
class TourTimeAdmin(admin.ModelAdmin):
    list_display = ("tour_date", "time")


@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ("tour", "image")


@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = ("full_name", "tour", "tour_date", "tour_time", "number_of_people", "is_paid", "created_at")
    list_filter = ("tour", "is_paid", "tour_date")
    search_fields = ("full_name", "phone_number", "email")

    def save_model(self, request, obj, form, change):
        remaining = obj.tour.remaining_capacity(obj.tour_date, exclude_booking=obj)
        if obj.number_of_people > remaining:
            raise ValidationError(
                f"ظرفیت باقی‌مانده این تور برای این تاریخ {remaining} نفر است."
            )
        super().save_model(request, obj, form, change)


# class TourBookingAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'tour', 'tour_date', 'number_of_people', 'is_paid')

#     def save_model(self, request, obj, form, change):
#         remaining = obj.tour.remaining_capacity(obj.tour_date)
#         if obj.number_of_people > remaining:
#             raise ValidationError(
#                 f"ظرفیت باقی‌مانده این تور برای این تاریخ {remaining} نفر است."
#             )
#         super().save_model(request, obj, form, change)

# admin.site.register(TourBooking, TourBookingAdmin)