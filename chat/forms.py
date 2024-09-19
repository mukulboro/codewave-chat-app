from django import forms
from django.core.exceptions import ValidationError

class ProfileUpdateForm(forms.Form):
    bio = forms.CharField(max_length=256, widget=forms.TextInput(attrs={
        "placeholder": "Add a bio...",
        "class": "input input-primary w-full max-w-md"
    }))
