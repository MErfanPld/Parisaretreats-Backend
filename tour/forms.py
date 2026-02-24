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

class TourBookingExtraForm(forms.ModelForm):
    class Meta:
        model = TourBooking
        fields = [
            "full_name",
            "phone_number",
            "email",
            "national_code",
            "passport_number",
            "birth_date",
            "gender",
            "has_medical_condition",
            "medical_condition_details",
            "has_allergy",
            "allergy_details",
            "can_swim",
            "drinks_alcohol",
            "smokes",
            "language_level",
            "emergency_contact_name",
            "emergency_contact_phone",
            "agree_to_terms",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
        labels = {
            "full_name": "Full Name",
            "phone_number": "Phone Number",
            "email": "Email",
            "national_code": "National Code",
            "passport_number": "Passport Number",
            "birth_date": "Birth Date",
            "gender": "Gender",
            "has_medical_condition": "Has Medical Condition?",
            "medical_condition_details": "Medical Condition Details",
            "has_allergy": "Has Allergy?",
            "allergy_details": "Allergy Details",
            "can_swim": "Can Swim?",
            "drinks_alcohol": "Drinks Alcohol?",
            "smokes": "Smokes?",
            "language_level": "Language Level",
            "emergency_contact_name": "Emergency Contact Name",
            "emergency_contact_phone": "Emergency Contact Phone",
            "agree_to_terms": "I agree to the Terms & Conditions",
        }

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if field.widget.__class__.__name__ != "CheckboxInput":
                field.widget.attrs.update({"class": "form-control"})
            else:
                field.widget.attrs.update({"class": "form-check-input"})
                
                
class ManualPaymentForm(forms.Form):
    receipt = forms.ImageField(label="upload")