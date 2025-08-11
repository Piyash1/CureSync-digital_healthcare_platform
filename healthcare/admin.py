from django.contrib import admin
from .models import *

admin.site.register(Profile)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'doctor_code']
    list_filter = ['specialization']
    search_fields = ['name', 'specialization', 'doctor_code']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'doctor', 'appointment_date', 'time_slot', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'doctor', 'created_at']
    search_fields = ['patient_name', 'patient_email', 'doctor__name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('user', 'patient_name', 'patient_email', 'patient_phone')
        }),
        ('Appointment Details', {
            'fields': ('doctor', 'appointment_date', 'time_slot', 'status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
