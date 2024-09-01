from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import viewsets

from .forms import CarForm, MaintenanceForm, ComplaintForm, ReferenceForm
from .models import Car, Maintenance, Complaint, Reference
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

from .serializers import CarSerializer, MaintenanceSerializer, ComplaintSerializer


def home(request):
    if request.user.is_authenticated:
        # Логика для авторизованных пользователей
        return redirect('authenticated_home')
    else:
        # Логика для неавторизованных пользователей
        return render(request, 'home.html')


def search_car(request):
    query = request.GET.get('query', '')
    cars = []
    message = ''
    if query:
        cars = Car.objects.filter(factory_number__icontains=query)[:10]
        if not cars:
            message = 'Данных о машине с таким заводским номером нет в системе'
    else:
        cars = Car.objects.all()[:10]

    return render(request, 'search_results.html', {'cars': cars, 'message': message})


def search_car2(request):
    query = request.GET.get('query', '')
    if query:
        cars = Car.objects.filter(factory_number__iexact=query)
    else:
        cars = Car.objects.all()[:10]
    return render(request, 'search_results.html', {'cars': cars})


def car_detail(request, car_id):
    try:
        car = get_object_or_404(Car, id=car_id)
        if not request.user.is_staff:
            if request.user.groups.filter(name='Клиент').exists() and car.client != request.user:
                raise Http404
            if request.user.groups.filter(name='Сервисная компания').exists() and car.service_company != request.user:
                raise Http404
        maintenances = Maintenance.objects.filter(car=car)
        complaints = Complaint.objects.filter(car=car)
        return render(request, 'car_detail.html', {
            'car': car,
            'maintenances': maintenances,
            'complaints': complaints
        })
    except Http404:
        return render(request, '404.html', status=404)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F
from .models import Car, Maintenance, Complaint


@login_required(login_url='home')
def authenticated_home(request):
    user = request.user
    if user.groups.filter(name='Клиент').exists():
        cars = Car.objects.filter(client=user)
    elif user.groups.filter(name='Сервисная компания').exists():
        cars = Car.objects.filter(service_company=user)
    elif user.is_staff:
        cars = Car.objects.all()
    else:
        cars = Car.objects.none()

    maintenances = Maintenance.objects.filter(car__in=cars).order_by('-date')
    complaints = Complaint.objects.filter(car__in=cars).order_by('-failure_date')

    # Фильтрация
    tech_model = request.GET.get('tech_model')
    engine_model = request.GET.get('engine_model')
    transmission_model = request.GET.get('transmission_model')
    drive_axle_model = request.GET.get('drive_axle_model')
    steering_axle_model = request.GET.get('steering_axle_model')
    active_tab = request.GET.get('active_tab', 'general')
    maintenance_type = request.GET.get('maintenance_type')

    if active_tab == 'general':
        if tech_model:
            cars = cars.filter(tech_model__name__icontains=tech_model)
        if engine_model:
            cars = cars.filter(engine_model__name__icontains=engine_model)
        if transmission_model:
            cars = cars.filter(transmission_model__name__icontains=transmission_model)
        if drive_axle_model:
            cars = cars.filter(drive_axle_model__name__icontains=drive_axle_model)
        if steering_axle_model:
            cars = cars.filter(steering_axle_model__name__icontains=steering_axle_model)
    elif active_tab == 'maintenance':
        if maintenance_type:
            maintenances = maintenances.filter(maintenance_type__name__icontains=maintenance_type)
        if engine_model:
            maintenances = maintenances.filter(car__engine_model__name__icontains=engine_model)
    elif active_tab == 'complaints':
        if tech_model:
            complaints = complaints.filter(car__tech_model__name__icontains=tech_model)
        if engine_model:
            complaints = complaints.filter(car__engine_model__name__icontains=engine_model)

    # Сортировка
    sort_by = request.GET.get('sort', 'shipping_date')
    if sort_by.startswith('-'):
        cars = cars.order_by(F(sort_by[1:]).desc(nulls_last=True))
    else:
        cars = cars.order_by(F(sort_by).asc(nulls_last=True))

    # Пагинация
    paginator = Paginator(cars, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Передача прав пользователя в контекст
    context = {
        'page_obj': page_obj,
        'maintenances': maintenances,
        'complaints': complaints,
        'active_tab': active_tab,
        'can_add_car': request.user.has_perm('app_name.can_add_car'),
        'can_change_car': request.user.has_perm('app_name.can_change_car'),
        'can_add_maintenance': request.user.has_perm('app_name.can_add_maintenance'),
        'can_change_maintenance': request.user.has_perm('app_name.can_change_maintenance'),
        'can_add_complaint': request.user.has_perm('app_name.can_add_complaint'),
        'can_change_complaint': request.user.has_perm('app_name.can_change_complaint'),
        'can_add_reference': request.user.has_perm('app_name.can_add_reference'),
        'can_change_reference': request.user.has_perm('app_name.can_change_reference'),
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'car_list.html', context)
    else:
        return render(request, 'authenticated_home.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Вы вошли как {username}.")
            return redirect('authenticated_home')
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    return render(request, 'base.html')


def reference_description(request):
    category = request.GET.get('category')
    name = request.GET.get('name')
    reference = Reference.objects.filter(category=category, name=name).first()

    if reference:
        context = {
            'reference': reference,
            'can_edit_reference': request.user.has_perm('app_name.can_change_reference')
        }
        return render(request, 'reference_detail.html', context)

    return JsonResponse({'description': 'Описание не найдено'})


def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('home')


def maintenance_detail(request, car_id, maintenance_id):
    maintenance = get_object_or_404(Maintenance, id=maintenance_id, car_id=car_id)
    return render(request, 'to_details.html', {'maintenance': maintenance})


def maintenance_details(request, maintenance_id):
    maintenance = get_object_or_404(Maintenance, id=maintenance_id)
    return render(request, 'to_details.html', {'maintenance': maintenance})


def complaint_detail(request, car_id, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id, car_id=car_id)
    return render(request, 'complaint_details.html', {'complaint': complaint})


def complaint_details(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    return render(request, 'complaint_details.html', {'complaint': complaint})


def reference_detail(request, category, name):
    reference = get_object_or_404(Reference, category=category, name=name)
    context = {
        'can_change_reference': request.user.has_perm('app_name.can_change_reference'),
    }
    return render(request, 'reference_details.html', {'reference': reference})


@permission_required('can_add_car')
def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CarForm()
    return render(request, 'create_edit_form.html', {'form': form})


@permission_required('can_change_car')
def edit_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CarForm(instance=car)
    return render(request, 'create_edit_form.html', {'form': form})


@permission_required('can_add_maintenance')
def create_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MaintenanceForm()
    return render(request, 'create_edit_form.html', {'form': form})


@permission_required('can_change_maintenance')
def edit_maintenance(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MaintenanceForm(instance=maintenance)
    return render(request, 'create_edit_form.html', {'form': form})


@permission_required('can_add_complaint')
def create_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ComplaintForm()
    return render(request, 'create_edit_form.html', {'form': form})


@permission_required('can_change_complaint')
def edit_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'create_edit_form.html', {'form': form})


@permission_required('can_add_reference')
def create_reference(request):
    if request.method == 'POST':
        form = ReferenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReferenceForm()
    return render(request, 'create_edit_form.html', {'form': form})


@permission_required('can_change_reference')
def edit_reference(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    if request.method == 'POST':
        form = ReferenceForm(request.POST, instance=reference)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReferenceForm(instance=reference)
    return render(request, 'create_edit_form.html', {'form': form})


class CarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class MaintenanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer


class ComplaintViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
