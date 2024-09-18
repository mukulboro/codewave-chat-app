from django import forms
from django.core.exceptions import ValidationError

class ProfileUpdateForm(forms.Form):
    bio = forms.CharField(max_length=256, widget=forms.TextInput(attrs={
        "placeholder": "Interests (comma separated)",
        "class": "input input-primary w-full max-w-md"
    }))

    updateName = forms.CharField(ax_length=32, widget=forms.TextInput(attrs={
        "placeholder": "Interests (comma separated)",
        "class": "input input-primary w-full max-w-md"
    }))