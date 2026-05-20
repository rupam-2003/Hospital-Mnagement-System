import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .models import Patient, Doctor, Appointment
from django.shortcuts import redirect
from .forms import DoctorForm, PatientForm, AppointmentForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Appointment
from .forms import AppointmentForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import PatientRegistrationForm
from django.contrib.auth import logout
from .models import Patient, Doctor, Appointment, SystemNotification

@login_required
def dashboard_view(request):
    total_patients = Patient.objects.count()
    active_doctors = Doctor.objects.filter(is_available=True).count()
    today_appointments = Appointment.objects.count()
    all_patients = Patient.objects.all()
    
    # FETCH LIVE UNREAD ALERTS LOGGED BY OUR SIGNALS
    live_notifications = SystemNotification.objects.filter(is_read=False)[:5]
    unread_count = live_notifications.count()

    context = {
        'total_patients': total_patients,
        'active_doctors': active_doctors,
        'today_appointments': today_appointments,
        'all_patients': all_patients,
        'notifications': live_notifications,
        'unread_count': unread_count,
    }
    return render(request, 'dashboard.html', context)

@login_required
def doctors_view(request):
    doctors = Doctor.objects.all()
    return render(request, 'core/doctors.html', {'doctors': doctors})

@login_required
def patients_view(request):
    patients = Patient.objects.all()
    return render(request, 'core/patients.html', {'patients': patients})

@login_required
def appointments_view(request):
    if request.user.is_staff:
        appointments = Appointment.objects.all()
    else:
        patient_profile = get_object_or_404(Patient, user=request.user)
        appointments = Appointment.objects.filter(patient=patient_profile)
        
    return render(request, 'core/appointments.html', {'appointments': appointments})


@login_required
def create_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            doctor = form.save(commit=False)
            doctor.user = user
            doctor.save()
            return redirect('doctors_list')
    else:
        form = DoctorForm()
    return render(request, 'core/form_template.html', {'form': form, 'title': 'Add New Doctor'})

@login_required
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            patient = form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect('patients_list')
    else:
        form = PatientForm()
    return render(request, 'core/form_template.html', {'form': form, 'title': 'Admit New Patient'})

@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            if not request.user.is_staff:
                appointment.patient = get_object_or_404(Patient, user=request.user)
            appointment.save()
            return redirect('appointments_list')
    else:
        form = AppointmentForm()
        if not request.user.is_staff:
            form.fields['patient'].widget = forms.HiddenInput()
            
    return render(request, 'core/form_template.html', {'form': form, 'title': 'Book Appointment'})

@login_required
def edit_appointment(request, appointment_id):
    # Check if the logged-in user is a hospital employee/admin
    if not request.user.is_staff:
        return HttpResponseForbidden("Access Denied: Only hospital employees can edit appointments.")
        
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments_list')
    else:
        form = AppointmentForm(instance=appointment)
        
    return render(request, 'core/form_template.html', {
        'form': form, 
        'title': f'Edit Appointment #{appointment.id}'
    })

def staff_login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'core/login.html', {
                    'form': form,
                    'error': 'Access Denied: This dashboard is restricted to hospital employees.'
                })
    else:
        form = AuthenticationForm()
        
    return render(request, 'core/login.html', {'form': form})

@login_required
def billing_view(request):
    # FIXED: Order by the related user's username instead of 'name'
    all_patients = Patient.objects.all().order_by('user__username') 
    
    context = {
        'patients': all_patients
    }
    return render(request, 'core/billing.html', context)

@login_required
def reports_view(request):
    return render(request, 'core/reports.html')

@login_required
def settings_view(request):
    return render(request, 'core/settings.html')

def logout_view(request):
    logout(request)
    return redirect('login')