from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('doctors/', views.doctors_view, name='doctors_list'),
    path('doctors/add/', views.create_doctor, name='create_doctor'),
    path('patients/', views.patients_view, name='patients_list'),
    path('patients/add/', views.create_patient, name='create_patient'),
    path('appointments/', views.appointments_view, name='appointments_list'),
    path('appointments/add/', views.create_appointment, name='create_appointment'),
    path('appointments/edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('', views.staff_login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('billing/', views.billing_view, name='billing'),
    path('reports/', views.reports_view, name='reports'),
    path('settings/', views.settings_view, name='settings'),
]