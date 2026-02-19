from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TourFeature(models.Model):
    name = models.CharField(max_length=100, verbose_name="ویژگی تور")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ویژگی تور"
        verbose_name_plural = "ویژگی‌های تور"


class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان تور")
    city = models.CharField(max_length=200, verbose_name="شهر")
    description = models.TextField(verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    features = models.ManyToManyField(
        TourFeature,
        related_name="tours",
        blank=True,
        verbose_name="ویژگی‌ها"
    )
    image = models.ImageField(upload_to="tour_images/", verbose_name="تصویر اصلی")
    capacity = models.PositiveIntegerField(default=10, verbose_name="ظرفیت تور")
    is_active = models.BooleanField(default=True, verbose_name="فعال باشد؟")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "تور"
        verbose_name_plural = "تور‌ها"


    def remaining_capacity(self, tour_date, exclude_booking=None):
        """
        تعداد نفرات باقی مانده برای یک تاریخ تور
        exclude_booking: اگر ویرایش رزرو باشد، آن رزرو را از جمع کنار بگذار
        """
        qs = self.bookings.filter(tour_date=tour_date)
        if exclude_booking:
            qs = qs.exclude(pk=exclude_booking.pk)
        total_reserved = qs.aggregate(total=models.Sum('number_of_people'))['total'] or 0
        return max(0, self.capacity - total_reserved)

class TourDate(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="dates", verbose_name="تور")
    start_date = models.DateField(verbose_name="تاریخ شروع")
    end_date = models.DateField(verbose_name="تاریخ پایان")

    def __str__(self):
        return f"{self.tour.title}: {self.start_date} - {self.end_date}"

    class Meta:
        verbose_name = "تاریخ تور"
        verbose_name_plural = "تاریخ‌های تور"


class TourTime(models.Model):
    tour_date = models.ForeignKey(TourDate, on_delete=models.CASCADE, related_name="times", verbose_name="تاریخ تور")
    time = models.TimeField(verbose_name="ساعت تور")

    def __str__(self):
        return f"{self.tour_date} @ {self.time}"

    class Meta:
        verbose_name = "ساعت تور"
        verbose_name_plural = "ساعت‌های تور"


class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="images", verbose_name="تور")
    image = models.ImageField(upload_to="tour_images/", verbose_name="تصویر")

    def __str__(self):
        return f"{self.tour.title} - Image"

    class Meta:
        verbose_name = "تصویر تور"
        verbose_name_plural = "تصاویر تور"


class TourBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کاربر")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    tour_date = models.ForeignKey(TourDate, on_delete=models.CASCADE, verbose_name="تاریخ تور")
    tour_time = models.ForeignKey(TourTime, on_delete=models.CASCADE, verbose_name="ساعت تور")
    full_name = models.CharField(max_length=150, verbose_name="نام کامل")
    phone_number = models.CharField(max_length=20, verbose_name="شماره تلفن")
    email = models.EmailField(verbose_name="ایمیل")

    can_swim = models.BooleanField(default=False, verbose_name="می‌تواند شنا کند؟")
    takes_medication = models.BooleanField(default=False, verbose_name="دارو مصرف می‌کند؟")
    medication_details = models.TextField(blank=True, null=True, verbose_name="توضیحات دارو")

    number_of_people = models.PositiveIntegerField(default=1, verbose_name="تعداد افراد")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ رزرو")
    is_paid = models.BooleanField(default=False, verbose_name="پرداخت شده؟")

    def __str__(self):
        return f"{self.full_name} - {self.tour.title} ({self.tour_date.start_date})"

    class Meta:
        verbose_name = "رزرو تور"
        verbose_name_plural = "رزروهای تور"


from django.contrib.auth import get_user_model

User = get_user_model()

class TourParticipant(models.Model):
    booking = models.ForeignKey("TourBooking", on_delete=models.CASCADE, related_name="participants", verbose_name="رزرو تور")
    full_name = models.CharField(max_length=150, verbose_name="نام کامل")
    phone_number = models.CharField(max_length=20, verbose_name="شماره تلفن")
    can_swim = models.BooleanField(default=False, verbose_name="می‌تواند شنا کند؟")
    takes_medication = models.BooleanField(default=False, verbose_name="دارو مصرف می‌کند؟")
    medication_details = models.TextField(blank=True, null=True, verbose_name="توضیحات دارو")
    accepted_terms = models.BooleanField(default=False, verbose_name="قوانین و شرایط را پذیرفته است")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    def __str__(self):
        return f"{self.full_name} ({self.booking.tour.title})"

    class Meta:
        verbose_name = "شرکت‌کننده تور"
        verbose_name_plural = "شرکت‌کنندگان تور"
