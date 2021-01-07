"""User forms."""

# Django
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Models
from django.contrib.auth.models import User
from users.models import Profile


class ProfileForm(forms.ModelForm):
    """Profile detail form."""

    class Meta:
        model = Profile
        fields = ('phone_number', 'picture') #Note that we didn't mention user field here.

    def save(self, user=None):
        user_profile = super(ProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile
