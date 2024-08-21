import django_filters
from .models import Car, Maintenance, Complaint


class CarFilter(django_filters.FilterSet):
    class Meta:
        model = Car
        fields = ['tech_model', 'engine_model', 'transmission_model', 'drive_axle_model', 'steering_axle_model']


class MaintenanceFilter(django_filters.FilterSet):
    class Meta:
        model = Maintenance
        fields = ['maintenance_type', 'car__factory_number', 'maintenance_organization']


class ComplaintFilter(django_filters.FilterSet):
    class Meta:
        model = Complaint
        fields = ['failure_node', 'recovery_method', 'car__factory_number', 'service_company']
