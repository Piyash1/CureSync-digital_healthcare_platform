from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required

def home_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def services_view(request):
    return render(request, 'services.html')

@login_required(login_url='/accounts/login/')
def booking_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            
            # Set the appointment_date from cleaned_data
            appointment.appointment_date = form.cleaned_data['appointment_date']
            
            # If user is logged in, associate the appointment with the user
            if request.user.is_authenticated:
                appointment.user = request.user
            
            appointment.save()
            
            messages.success(
                request, 
                f'Appointment booked successfully for {appointment.appointment_date} '
                f'at {appointment.get_time_slot_display()} with {appointment.doctor.name}.'
            )
            return redirect('booking')
        else:
            messages.error(request, 'Please correct the errors below.')
            # Debug: Print form errors
            print("Form errors:", form.errors)
            print("Form cleaned_data:", form.cleaned_data)
    else:
        form = AppointmentForm()
    
    # Get upcoming appointments
    if request.user.is_authenticated:
        upcoming_appointments = Appointment.objects.filter(
            user=request.user,
            appointment_date__gte=timezone.now().date(),
            status__in=['pending', 'confirmed']
        ).order_by('appointment_date', 'time_slot')
    else:
        # For anonymous users, you might want to store appointments in session
        # For now, we'll show empty list
        upcoming_appointments = []
    
    context = {
        'form': form,
        'upcoming_appointments': upcoming_appointments,
    }
    
    return render(request, 'booking.html', context)

@login_required(login_url='/accounts/login/')
def cancel_appointment(request, appointment_id):
    """View to cancel an appointment"""
    try:
        if request.user.is_authenticated:
            appointment = Appointment.objects.get(
                id=appointment_id, 
                user=request.user,
                status__in=['pending', 'confirmed']
            )
            appointment.status = 'cancelled'
            appointment.save()
            messages.success(request, 'Appointment cancelled successfully.')
        else:
            messages.error(request, 'You must be logged in to cancel appointments.')
    except Appointment.DoesNotExist:
        messages.error(request, 'Appointment not found or cannot be cancelled.')
    
    return redirect('booking')