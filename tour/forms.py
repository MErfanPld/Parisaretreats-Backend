from django import forms
from .models import TourBooking

class TourBookingForm(forms.ModelForm):
    class Meta:
        model = TourBooking
        # fields = ["full_name", "phone_number", "email", "number_of_people"]
        fields = ["full_name", "phone_number"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            # "email": forms.EmailInput(attrs={"class": "form-control"}),
            # "number_of_people": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }

