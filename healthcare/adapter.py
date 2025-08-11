from allauth.account.adapter import DefaultAccountAdapter
from django.utils.text import slugify
from django.contrib.auth.models import User

class CustomAccountAdapter(DefaultAccountAdapter):
    def generate_unique_username(self, base_username):
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        return username

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)

        # Generate username from email or name
        email = form.cleaned_data.get('email')
        base_username = slugify(email.split('@')[0]) if email else 'user'
        user.username = self.generate_unique_username(base_username)

        # Save full name if provided
        name = form.cleaned_data.get('name')
        if name:
            user.first_name = name

        if commit:
            user.save()

        return user
