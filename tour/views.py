from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from .models import BankAccount, Tour, TourBooking, TourDate, TourTime
from .forms import ManualPaymentForm, TourBookingExtraForm, TourBookingForm

class TourListView(ListView):
    model = Tour
    template_name = "tour/tour_list.html"
    context_object_name = "tours"
    queryset = Tour.objects.filter(is_active=True)



from django.shortcuts import redirect, get_object_or_404

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, FormView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tour, TourBooking, TourDate, TourTime, BankAccount
from .forms import TourBookingForm, TourBookingExtraForm, ManualPaymentForm


# ------------------------------
# مرحله 0: لیست تورها
# ------------------------------
class TourListView(ListView):
    model = Tour
    template_name = "tour/tour_list.html"
    context_object_name = "tours"
    queryset = Tour.objects.filter(is_active=True)


# ------------------------------
# مرحله 1: جزئیات تور و فرم رزرو اولیه
# ------------------------------
class TourDetailView(DetailView):
    model = Tour
    template_name = "tour/tour_detail.html"
    context_object_name = "tour"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dates"] = self.object.dates.all()
        context["images"] = self.object.images.all()
        context["form"] = TourBookingForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not request.user.is_authenticated:
            return redirect(f"/accounts/login/?next={request.path}")

        form = TourBookingForm(request.POST)
        tour_date_id = request.POST.get("tour_date")
        tour_time_id = request.POST.get("tour_time")

        if form.is_valid():
            tour_date = get_object_or_404(TourDate, id=tour_date_id)
            requested_people = form.cleaned_data.get("number_of_people", 1)
            remaining = self.object.remaining_capacity(tour_date)

            if requested_people > remaining:
                form.add_error(
                    "number_of_people",
                    f"Remaining capacity is {remaining}"
                )
                context = self.get_context_data()
                context["form"] = form
                return self.render_to_response(context)

            # ذخیره مرحله اول (فقط فیلدهای validated)
            request.session["booking_step1"] = {
                "tour_id": self.object.id,
                "tour_date_id": tour_date.id,
                "tour_time_id": tour_time_id,
                "data": {
                    "full_name": form.cleaned_data["full_name"],
                    "phone_number": form.cleaned_data["phone_number"],
                    "number_of_people": requested_people,
                },
            }

            return redirect("tours:booking_extra")

        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


import datetime
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TourBooking, BankAccount, TourDate, TourTime
from .forms import TourBookingExtraForm, ManualPaymentForm


# ------------------------------
# مرحله 2: اطلاعات اضافی
# ------------------------------
class TourBookingExtraView(LoginRequiredMixin, FormView):
    template_name = "tour/booking_extra.html"
    form_class = TourBookingExtraForm

    def form_valid(self, form):
        step1 = self.request.session.get("booking_step1")
        if not step1:
            return redirect("tours:tour_list")

        # فقط مقادیری که JSON-serializable هستند
        step2 = {}
        for key, value in form.cleaned_data.items():
            if isinstance(value, (str, int, float, bool)):
                step2[key] = value
            elif isinstance(value, type(None)):
                step2[key] = None
            else:
                # date یا datetime → تبدیل به string
                step2[key] = str(value)

        self.request.session["booking_step2"] = step2
        return redirect("tours:manual_payment")


# ------------------------------
# مرحله 3: پرداخت دستی
# ------------------------------
class ManualPaymentView(LoginRequiredMixin, FormView):
    template_name = "tour/manual_payment.html"
    form_class = ManualPaymentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bank_accounts"] = BankAccount.objects.all()
        return context

    def form_valid(self, form):
        step1 = self.request.session.get("booking_step1")
        step2 = self.request.session.get("booking_step2") or {}

        if not step1:
            return redirect("tours:tour_list")

        # تبدیل رشته‌های date دوباره به date واقعی
        birth_date_str = step2.get("birth_date")
        birth_date = datetime.datetime.strptime(birth_date_str, "%Y-%m-%d").date() if birth_date_str else None

        # تبدیل boolean ها
        def get_bool(key):
            val = step2.get(key)
            return val in [True, "True", "on"]

        # ساخت رزرو نهایی
        booking = TourBooking.objects.create(
            user=self.request.user,
            tour_id=step1["tour_id"],
            tour_date_id=step1["tour_date_id"],
            tour_time_id=step1["tour_time_id"],
            payment_receipt=form.cleaned_data["receipt"],

            # مرحله اول
            full_name=step1["data"]["full_name"],
            phone_number=step1["data"]["phone_number"],
            number_of_people=step1["data"]["number_of_people"],

            # مرحله دوم
            national_code=step2.get("national_code"),
            passport_number=step2.get("passport_number"),
            birth_date=birth_date,
            gender=step2.get("gender"),
            can_swim=get_bool("can_swim"),
            takes_medication=get_bool("takes_medication"),
            medication_details=step2.get("medication_details"),
            has_medical_condition=get_bool("has_medical_condition"),
            medical_condition_details=step2.get("medical_condition_details"),
            has_allergy=get_bool("has_allergy"),
            allergy_details=step2.get("allergy_details"),
            emergency_contact_name=step2.get("emergency_contact_name"),
            emergency_contact_phone=step2.get("emergency_contact_phone"),
            drinks_alcohol=get_bool("drinks_alcohol"),
            smokes=get_bool("smokes"),
            language_level=step2.get("language_level"),
            agree_to_terms=True,
        )

        # پاک کردن session بعد از ذخیره
        self.request.session.pop("booking_step1", None)
        self.request.session.pop("booking_step2", None)

        return redirect("tours:booking_success")


# ------------------------------
# مرحله 4: صفحه موفقیت
# ------------------------------
class BookingSuccessView(TemplateView):
    template_name = "tour/booking_success.html"
