from django.contrib import admin

from .models import Reference, Car, Maintenance, Complaint

# Register your models here.
admin.site.register(Reference)
admin.site.register(Car)
admin.site.register(Maintenance)
admin.site.register(Complaint)