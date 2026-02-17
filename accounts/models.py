import time
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from .managers import UserManager
from .validator import *
from extenstions.utils import jalali_converter

def upload_image(instance, filename):
    identifier = instance.email or instance.phone_number
    path = f"uploads/users/{slugify(identifier, allow_unicode=True)}"
    name = f"{int(time.time())}-{filename}"
    return f"{path}/{name}"

class User(AbstractBaseUser, PermissionsMixin):
    # Basic info
    first_name = models.CharField(_("نام"), max_length=100)
    last_name = models.CharField(_("نام خانوادگی"), max_length=100)
    phone_number = models.CharField(
        _("شماره تلفن"),
        max_length=15, 
        unique=True,
        validators=[mobile_validator]
    )
    email = models.EmailField(_("ایمیل"), unique=True, null=True, blank=True)
    telegram_id = models.CharField(_("تلگرام آی‌دی"), max_length=50, null=True, blank=True)
    bio = models.TextField(_("بایو"), null=True, blank=True)
    image = models.ImageField(_("تصویر"), upload_to=upload_image, null=True, blank=True)

    # Permissions
    is_owner = models.BooleanField(_("مالک هست؟"), default=False)
    is_staff = models.BooleanField(_("کارمند"), default=False)
    is_superuser = models.BooleanField(_("ادمین هست؟"), default=False)
    is_active = models.BooleanField(_("فعال"), default=True)

    # Dates
    created_at = models.DateTimeField(_("تاریخ ثبت"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاریخ ویرایش"), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email or self.phone_number or "---"

    def get_avatar(self):
        return self.image.url if self.image else "/static/img/user-3.jpg"

    def jcreated(self):
        return jalali_converter(self.created_at)

    # Validation
    def clean(self):
        if self.phone_number:
            self.phone_number = mobile_validator(str(self.phone_number)[:11])
            qs = User.objects.filter(phone_number=self.phone_number)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(_("شماره موبایل تکراری است!"), code="mobile")

        if self.email:
            qs = User.objects.filter(email=self.email)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(_("ایمیل تکراری است!"), code="email")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
