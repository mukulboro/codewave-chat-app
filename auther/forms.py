from django import forms
from django.core.exceptions import ValidationError


GENDER_CHOICES= (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('LGBTQIA+', 'LGBTQIA+'),
)

class UserRegistrationForm(forms.Form):

    first_name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={
        "placeholder": "First Name",
        "class": "input input-primary w-full max-w-md"
    }))
    last_name = forms.CharField(max_length=32, widget=forms.TextInput(attrs={
        "placeholder": "Last Name",
        "class": "input input-primary w-full max-w-md"
    }))
    email = forms.EmailField(max_length=256, widget=forms.EmailInput(attrs={
        "placeholder": "Email",
        "class": "input input-primary w-full max-w-md"
    }))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={
        "placeholder": "Age",
        "class": "input input-primary w-full max-w-md"
    }))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={
        "class": "select select-primary w-full max-w-md"
    }))
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "input input-primary w-full max-w-md"
    }))
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm Password",
        "class": "input input-primary w-full max-w-md"
    }))
    location = forms.CharField(max_length=52, widget=forms.TextInput(attrs={
        "placeholder": "Location",
        "class": "input input-primary w-full max-w-md"
    }))
    interests = forms.CharField(max_length=512, widget=forms.TextInput(attrs={
        "placeholder": "Interests (comma separated)",
        "class": "input input-primary w-full max-w-md"
    }))
    profile_picture = forms.ImageField(required=True, widget=forms.FileInput(attrs={
        "class": "file-input file-input-primary w-full max-w-md"
    }))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return cleaned_data

    

    
    
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=256,  widget=forms.EmailInput(attrs={
        "placeholder": "Type Here",
        "class": "input input-bordered input-primary w-full max-w-xs"
    }))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={
        "placeholder": "Type Here",
        "class": "input input-bordered input-primary w-full max-w-xs"
    }))

class TwoFactorForm(forms.Form):
    token = forms.IntegerField(widget=forms.NumberInput(attrs={
        "placeholder":"type here",
        "class": "input input-primary w-full max-w-md font-semibold"
    }))