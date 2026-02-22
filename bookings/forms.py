from django import forms
from .models import Booking, Circuit

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['circuit', 'hotel_tier', 'transport_choice', 'start_date', 'duration_days']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'duration_days': forms.NumberInput(attrs={'min': 2, 'class': 'form-control'}),
            'circuit': forms.Select(attrs={'class': 'form-select'}),
            'hotel_tier': forms.Select(attrs={'class': 'form-select'}),
            'transport_choice': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        package = kwargs.pop('package', None)
        super().__init__(*args, **kwargs)
        if package:
            # Explicitly setting the queryset based on the related_name defined in models.py
            self.fields['circuit'].queryset = package.circuits.all()