from allauth.account.forms import SignupForm
from django import forms
from .models import *
from datetime import datetime, timedelta

class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=150, label='Full Name', required=True)
    age = forms.IntegerField(label='Age', required=False)
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, label='Gender', required=False)
    mobile = forms.CharField(max_length=20, label='Mobile Number', required=False)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['name']
        user.save()

        Profile.objects.create(
            user=user,
            age=self.cleaned_data.get('age'),
            gender=self.cleaned_data.get('gender'),
            mobile=self.cleaned_data.get('mobile'),
        )
        return user
    
class AppointmentForm(forms.ModelForm):
    day = forms.ChoiceField(choices=[], required=True)
    month = forms.ChoiceField(choices=[], required=True)
    year = forms.ChoiceField(choices=[], required=True)
    
    class Meta:
        model = Appointment
        fields = ['patient_name', 'patient_email', 'patient_phone', 'doctor', 'time_slot', 'notes']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'patient_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'patient_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'time_slot': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any additional notes (optional)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Generate day choices (1-31)
        day_choices = [('', 'Day')] + [(str(i), str(i)) for i in range(1, 32)]
        self.fields['day'].choices = day_choices
        
        # Generate month choices
        month_choices = [('', 'Month')] + [
            ('01', 'January'), ('02', 'February'), ('03', 'March'),
            ('04', 'April'), ('05', 'May'), ('06', 'June'),
            ('07', 'July'), ('08', 'August'), ('09', 'September'),
            ('10', 'October'), ('11', 'November'), ('12', 'December')
        ]
        self.fields['month'].choices = month_choices
        
        # Generate year choices (current year and next year)
        current_year = timezone.now().year
        year_choices = [('', 'Year')] + [(str(year), str(year)) for year in range(current_year, current_year + 2)]
        self.fields['year'].choices = year_choices
        
        # Set doctor choices
        self.fields['doctor'].queryset = Doctor.objects.all()
        self.fields['doctor'].empty_label = "Choose a doctor"
    
    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        month = cleaned_data.get('month')
        year = cleaned_data.get('year')
        doctor = cleaned_data.get('doctor')
        time_slot = cleaned_data.get('time_slot')
        
        # Validate and create appointment_date
        if day and month and year:
            try:
                # Ensure day is zero-padded
                day_str = day.zfill(2)
                appointment_date = datetime.strptime(f'{year}-{month}-{day_str}', '%Y-%m-%d').date()
                
                # Check if date is not in the past
                if appointment_date < timezone.now().date():
                    raise forms.ValidationError("Cannot book appointments for past dates.")
                
                # Check if the slot is already booked
                if doctor and time_slot:
                    existing_appointment = Appointment.objects.filter(
                        doctor=doctor,
                        appointment_date=appointment_date,
                        time_slot=time_slot
                    ).first()
                    
                    if existing_appointment:
                        raise forms.ValidationError("This time slot is already booked for the selected doctor.")
                
                cleaned_data['appointment_date'] = appointment_date
                
            except ValueError:
                raise forms.ValidationError("Please enter a valid date.")
        else:
            raise forms.ValidationError("Please select a complete date (day, month, and year).")
        
        return cleaned_data