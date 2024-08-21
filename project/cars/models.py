from django.db import models
from django.contrib.auth.models import User


# Справочники
class Reference(models.Model):
    CATEGORIES = [
        ('Модель техники', 'Модель техники'),
        ('Модель двигателя', 'Модель двигателя'),
        ('Модель трансмиссии', 'Модель трансмиссии'),
        ('Модель ведущего моста', 'Модель ведущего моста'),
        ('Модель управляемого моста', 'Модель управляемого моста'),
        ('Вид ТО', 'Вид ТО'),
        ('Организация, проводившая ТО', 'Организация, проводившая ТО'),
        ('Узел отказа', 'Узел отказа'),
        ('Способ восстановления', 'Способ восстановления'),
    ]
    category = models.CharField(max_length=100, choices=CATEGORIES)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.category} - {self.name}"


# Модель Машины
class Car(models.Model):
    factory_number = models.CharField(max_length=255, unique=True, verbose_name="Зав. № машины")
    tech_model = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True, related_name='car_tech_models',
                                   limit_choices_to={'category': 'Модель техники'}, verbose_name="Модель техники")
    engine_model = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True, related_name='car_engine_models',
                                     limit_choices_to={'category': 'Модель двигателя'}, verbose_name="Модель двигателя")
    engine_number = models.CharField(max_length=255, verbose_name="Зав. № двигателя")
    transmission_model = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True,
                                           related_name='car_transmission_models',
                                           limit_choices_to={'category': 'Модель трансмиссии'}, verbose_name="Модель трансмиссии")
    transmission_number = models.CharField(max_length=255, verbose_name="Зав. № трансмиссии")
    drive_axle_model = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True,
                                         related_name='car_drive_axle_models',
                                         limit_choices_to={'category': 'Модель ведущего моста'}, verbose_name="Модель ведущего моста")
    drive_axle_number = models.CharField(max_length=255, verbose_name="Зав. № ведущего моста")
    steering_axle_model = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True,
                                            related_name='car_steering_axle_models',
                                            limit_choices_to={'category': 'Модель управляемого моста'}, verbose_name="Модель управляемого моста")
    steering_axle_number = models.CharField(max_length=255, verbose_name="Зав. № управляемого моста")
    supply_contract = models.CharField(max_length=255, verbose_name="Договор поставки №, дата")
    shipping_date = models.DateField(verbose_name="Дата отгрузки с завода")
    consignee = models.CharField(max_length=255, verbose_name="Грузополучатель (конечный потребитель)")
    delivery_address = models.CharField(max_length=255, verbose_name="Адрес поставки (эксплуатации)")
    equipment = models.TextField(verbose_name="Комплектация (доп. опции)")
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='client_cars', verbose_name="Клиент")
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='service_company_cars', verbose_name="Сервисная компания")

    def __str__(self):
        return f"Car {self.factory_number}"


class Maintenance(models.Model):
    maintenance_type = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True,
                                         related_name='maintenance_types',
                                         limit_choices_to={'category': 'Вид ТО'}, verbose_name="Вид ТО")
    date = models.DateField(verbose_name="Дата проведения ТО")
    operating_time = models.FloatField(verbose_name="Наработка, м/час")
    order_number = models.CharField(max_length=255, verbose_name="№ заказ-наряда")
    order_date = models.DateField(verbose_name="Дата заказ-наряда")
    maintenance_organization = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True,
                                                 related_name='maintenance_organizations',
                                                 limit_choices_to={'category': 'Организация, проводившая ТО'}, verbose_name="Организация, проводившая ТО")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='maintenances', verbose_name="Машина")
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                        related_name='maintenance_service_companies', verbose_name="Сервисная компания")

    def __str__(self):
        return f"Maintenance for {self.car.factory_number} on {self.date}"


class Complaint(models.Model):
    failure_date = models.DateField(verbose_name="Дата отказа")
    operating_time = models.FloatField(verbose_name="Наработка, м/час")
    failure_node = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True, related_name='failure_nodes',
                                     limit_choices_to={'category': 'Узел отказа'}, verbose_name="Узел отказа")
    failure_description = models.TextField(verbose_name="Описание отказа")
    recovery_method = models.ForeignKey(Reference, on_delete=models.SET_NULL, null=True,
                                        related_name='recovery_methods',
                                        limit_choices_to={'category': 'Способ восстановления'}, verbose_name="Способ восстановления")
    parts_used = models.TextField(verbose_name="Используемые запасные части")
    recovery_date = models.DateField(verbose_name="Дата восстановления")
    downtime = models.FloatField(verbose_name="Время простоя техники")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='complaints', verbose_name="Машина")
    service_company = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                        related_name='complaint_service_companies', verbose_name="Сервисная компания")

    def __str__(self):
        return f"Complaint for {self.car.factory_number} on {self.failure_date}"

    def save(self, *args, **kwargs):
        if self.recovery_date and self.failure_date:
            self.downtime = (self.recovery_date - self.failure_date).days
        super().save(*args, **kwargs)


