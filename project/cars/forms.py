from django import forms
from .models import Car, Maintenance, Complaint, Reference


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = '__all__'


class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = '__all__'
