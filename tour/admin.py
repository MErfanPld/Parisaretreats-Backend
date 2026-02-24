from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from django.forms import ValidationError
from .models import (
    Tour,
    TourDate,
    TourFeature,
    TourTime,
    TourImage,
    TourBooking,
    BankAccount,
)

# ===============================
# Inline ها
# ===============================

class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1


class TourTimeInline(admin.TabularInline):
    model = TourTime
    extra = 1


class TourDateInline(admin.TabularInline):
    model = TourDate
    extra = 1


# ===============================
# Tour Feature
# ===============================

@admin.register(TourFeature)
class TourFeatureAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ===============================
# Tour
# ===============================

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "price",
        "capacity",
        "remaining_capacity_display",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "city")
    search_fields = ("title", "city")
    filter_horizontal = ("features",)
    inlines = [TourDateInline, TourImageInline]
    readonly_fields = ("created_at",)

    def remaining_capacity_display(self, obj):
        total_reserved = obj.bookings.aggregate(
            total=Sum("number_of_people")
        )["total"] or 0
        remaining = obj.capacity - total_reserved

        color = "green" if remaining > 0 else "red"
        return format_html(
            '<span style="color:{}; font-weight:bold;">{} نفر</span>',
            color,
            remaining,
        )

    remaining_capacity_display.short_description = "ظرفیت باقی‌مانده"


# ===============================
# Tour Date
# ===============================

@admin.register(TourDate)
class TourDateAdmin(admin.ModelAdmin):
    list_display = ("tour", "start_date", "end_date")
    list_filter = ("tour",)
    inlines = [TourTimeInline]


# ===============================
# Tour Time
# ===============================

@admin.register(TourTime)
class TourTimeAdmin(admin.ModelAdmin):
    list_display = ("tour_date", "time")
    list_filter = ("tour_date",)


# ===============================
# Tour Image
# ===============================

@admin.register(TourImage)
class TourImageAdmin(admin.ModelAdmin):
    list_display = ("tour", "image")


# ===============================
# Bank Account
# ===============================

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("bank_name", "card_number", "account_holder")
    search_fields = ("bank_name", "card_number", "account_holder")


# ===============================
# Tour Booking (پیشرفته)
# ===============================

@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "tour",
        "tour_date",
        "tour_time",
        "number_of_people",
        "payment_status",
        "created_at",
    )

    list_filter = ("tour", "tour_date", "is_paid", "created_at")
    search_fields = ("full_name", "phone_number", "email")
    readonly_fields = ("created_at", "receipt_preview")

    fieldsets = (
        ("اطلاعات اصلی", {
            "fields": (
                "user",
                "tour",
                "tour_date",
                "tour_time",
                "number_of_people",
            )
        }),
        ("اطلاعات تماس", {
            "fields": (
                "full_name",
                "phone_number",
                "email",
            )
        }),
        ("اطلاعات پزشکی", {
            "fields": (
                "can_swim",
                "takes_medication",
                "medication_details",
                "has_medical_condition",
                "medical_condition_details",
                "has_allergy",
                "allergy_details",
            )
        }),
        ("پرداخت", {
            "fields": (
                "payment_receipt",
                "receipt_preview",
                "is_paid",
            )
        }),
        ("سایر", {
            "fields": (
                "agree_to_terms",
                "created_at",
            )
        }),
    )

    # رنگی کردن وضعیت پرداخت
    def payment_status(self, obj):
        if obj.is_paid:
            return format_html(
                '<span style="color:green; font-weight:bold;">پرداخت شده</span>'
            )
        return format_html(
            '<span style="color:red; font-weight:bold;">در انتظار پرداخت</span>'
        )

    payment_status.short_description = "وضعیت پرداخت"

    # پیش نمایش فیش
    def receipt_preview(self, obj):
        if obj.payment_receipt:
            return format_html(
                '<img src="{}" width="200" style="border-radius:10px;" />',
                obj.payment_receipt.url
            )
        return "فیشی ثبت نشده"

    receipt_preview.short_description = "پیش‌نمایش فیش"

    # کنترل ظرفیت هنگام ذخیره
    def save_model(self, request, obj, form, change):
        remaining = obj.tour.remaining_capacity(
            obj.tour_date,
            exclude_booking=obj if change else None
        )

        if obj.number_of_people > remaining:
            raise ValidationError(
                f"ظرفیت باقی‌مانده این تور {remaining} نفر است."
            )

        super().save_model(request, obj, form, change)
