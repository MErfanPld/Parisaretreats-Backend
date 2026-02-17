import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# -----------------------------
# Regex چندکشوره
# -----------------------------
mobile_patterns = {
    "iran": re.compile(r'^(?:\+98|0)?9\d{9}$'),
    "turkey": re.compile(r'^(?:\+90|0)?5\d{9}$'),
    "usa": re.compile(r'^(?:\+1|1)?\d{10}$'),
    "uk": re.compile(r'^(?:\+44|0)?7\d{9}$'),
}

def mobile_validator(value):
    """
    بررسی شماره موبایل چندکشوره
    ایران، ترکیه، آمریکا، انگلیس
    مقدار صحیح را برمی‌گرداند یا ValidationError می‌دهد
    """
    value = str(value).replace(" ", "").replace("-", "").strip()
    
    for country, pattern in mobile_patterns.items():
        if pattern.match(value):
            return value
    
    raise ValidationError(
        _("شماره موبایل نامعتبر است! باید ایران، ترکیه، آمریکا یا انگلیس باشد."),
        code='invalid_mobile'
    )
