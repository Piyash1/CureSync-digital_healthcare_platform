from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    mobile = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.email or self.user.username
    
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    doctor_code = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.name} ({self.specialization})"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    TIME_SLOTS = [
        ('09:00-10:00', '09:00 AM - 10:00 AM'),
        ('10:00-11:00', '10:00 AM - 11:00 AM'),
        ('11:00-12:00', '11:00 AM - 12:00 PM'),
        ('13:00-14:00', '01:00 PM - 02:00 PM'),
        ('14:00-15:00', '02:00 PM - 03:00 PM'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=15)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['doctor', 'appointment_date', 'time_slot']
        ordering = ['appointment_date', 'time_slot']
    
    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name} on {self.appointment_date} at {self.time_slot}"
    
    @property
    def is_upcoming(self):
        return self.appointment_date >= timezone.now().date() and self.status in ['pending', 'confirmed']
