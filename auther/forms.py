from django import forms
from django.core.exceptions import ValidationError


GENDER_CHOICES= (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('LGBTQIA+', 'LGBTQIA+'),
)

class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=256)
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput)
    location = forms.CharField(max_length=52)
    interests = forms.CharField(max_length=512) # Take in comma seperated values
    profile_picture = forms.ImageField(required=True)
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return cleaned_data
    
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=256)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class TwoFactorForm(forms.Form):
    token = forms.IntegerField()