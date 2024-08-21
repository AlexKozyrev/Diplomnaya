from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Car, Maintenance, Complaint
from .filters import CarFilter, MaintenanceFilter, ComplaintFilter


@login_required
def dashboard(request):
    user = request.user
    cars = Car.objects.none()
    maintenances = Maintenance.objects.none()
    complaints = Complaint.objects.none()

    if user.groups.filter(name='Client').exists():
        cars = Car.objects.filter(client=user)
        maintenances = Maintenance.objects.filter(car__client=user)
        complaints = Complaint.objects.filter(car__client=user)
    elif user.groups.filter(name='Service Organization').exists():
        cars = Car.objects.filter(service_company=user)
        maintenances = Maintenance.objects.filter(service_company=user)
        complaints = Complaint.objects.filter(service_company=user)
    elif user.groups.filter(name='Manager').exists():
        cars = Car.objects.all()
        maintenances = Maintenance.objects.all()
        complaints = Complaint.objects.all()

    car_filter = CarFilter(request.GET, queryset=cars)
    maintenance_filter = MaintenanceFilter(request.GET, queryset=maintenances)
    complaint_filter = ComplaintFilter(request.GET, queryset=complaints)

    context = {
        'cars': car_filter.qs,
        'maintenances': maintenance_filter.qs,
        'complaints': complaint_filter.qs,
        'car_filter': car_filter,
        'maintenance_filter': maintenance_filter,
        'complaint_filter': complaint_filter,
    }

    return render(request, 'dashboard.html', context)


def search_car(request):
    if request.method == 'POST':
        factory_number = request.POST.get('factory_number')
        try:
            car = Car.objects.get(factory_number=factory_number)
            return render(request, 'car_detail.html', {'car': car})
        except Car.DoesNotExist:
            return render(request, 'car_not_found.html')
    return render(request, 'search_car.html')


def car_detail_public(request, pk):
    car = get_object_or_404(Car, pk=pk)
    # Возвращаем только поля пп.1-10
    public_fields = ['field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7', 'field8', 'field9',
                     'field10']
    car_data = {field: getattr(car, field) for field in public_fields}
    return JsonResponse(car_data)
