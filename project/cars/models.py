from django.db import models
from django.contrib.auth.models import User


# Справочники
class Reference(models.Model):
    entity_name = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Модель Машины
class Car(models.Model):
    factory_number = models.CharField(max_length=255, unique=True)
    tech_model = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True, related_name='car_tech_models')
    engine_model = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True, related_name='car_engine_models')
    engine_number = models.CharField(max_length=255)
    transmission_model = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True,
                                           related_name='car_transmission_models')
    transmission_number = models.CharField(max_length=255)
    drive_axle_model = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True,
                                         related_name='car_drive_axle_models')
    drive_axle_number = models.CharField(max_length=255)
    steering_axle_model = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True,
                                            related_name='car_steering_axle_models')
    steering_axle_number = models.CharField(max_length=255)
    supply_contract = models.CharField(max_length=255)
    shipping_date = models.DateField()
    consignee = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    equipment = models.TextField()
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='client_cars')
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='service_company_cars')

    def __str__(self):
        return f"Car {self.factory_number}"


# Модель ТО (Техническое обслуживание)
class Maintenance(models.Model):
    maintenance_type = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True,
                                         related_name='maintenance_types')
    date = models.DateField()
    operating_time = models.FloatField()
    order_number = models.CharField(max_length=255)
    order_date = models.DateField()
    maintenance_organization = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True,
                                                 related_name='maintenance_organizations')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='maintenances')
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                        related_name='maintenance_service_companies')

    def __str__(self):
        return f"Maintenance for {self.car.factory_number} on {self.date}"


# Модель Рекламации
class Complaint(models.Model):
    failure_date = models.DateField()
    operating_time = models.FloatField()
    failure_node = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True, related_name='failure_nodes')
    failure_description = models.TextField()
    recovery_method = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True,
                                        related_name='recovery_methods')
    parts_used = models.TextField()
    recovery_date = models.DateField()
    downtime = models.FloatField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='complaints')
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                        related_name='complaint_service_companies')

    def __str__(self):
        return f"Complaint for {self.car.factory_number} on {self.failure_date}"

    def save(self, *args, **kwargs):
        if self.recovery_date and self.failure_date:
            self.downtime = (self.recovery_date - self.failure_date).days
        super().save(*args, **kwargs)