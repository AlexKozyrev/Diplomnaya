from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Car, Maintenance, Complaint, Reference

# Создаем группы
client_group, created = Group.objects.get_or_create(name='Client')
service_group, created = Group.objects.get_or_create(name='Service Organization')
manager_group, created = Group.objects.get_or_create(name='Manager')

# Получаем ContentType для моделей
car_content_type = ContentType.objects.get_for_model(Car)
maintenance_content_type = ContentType.objects.get_for_model(Maintenance)
complaint_content_type = ContentType.objects.get_for_model(Complaint)
reference_content_type = ContentType.objects.get_for_model(Reference)

# Создаем разрешения
view_car = Permission.objects.get(codename='view_car', content_type=car_content_type)
change_car = Permission.objects.get(codename='change_car', content_type=car_content_type)
view_maintenance = Permission.objects.get(codename='view_maintenance', content_type=maintenance_content_type)
change_maintenance = Permission.objects.get(codename='change_maintenance', content_type=maintenance_content_type)
view_complaint = Permission.objects.get(codename='view_complaint', content_type=complaint_content_type)
change_complaint = Permission.objects.get(codename='change_complaint', content_type=complaint_content_type)
change_reference = Permission.objects.get(codename='change_reference', content_type=reference_content_type)

# Назначаем разрешения группам
client_group.permissions.add(view_car, view_maintenance, change_maintenance, view_complaint)
service_group.permissions.add(view_car, view_maintenance, change_maintenance, view_complaint, change_complaint)
manager_group.permissions.add(view_car, change_car, view_maintenance, change_maintenance, view_complaint, change_complaint, change_reference)