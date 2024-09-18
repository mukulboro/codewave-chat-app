from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm, TwoFactorForm
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.utils.crypto import get_random_string
from .utils import generate_qr, generate_totp
from .models import UserInterests, PublicUser

def register_view(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {
            "form": form
        }
        return render(request, "register.html", context=context)
    
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        User = get_user_model()
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            age = form.cleaned_data.get("age")
            password = form.cleaned_data.get("password1")
            random_username = get_random_string(length=32)
            interests = form.cleaned_data.get("interests")
            location = form.cleaned_data.get("location")
            gender = form.cleaned_data.get("gender")
            interest_list = interests.split(",")
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                age=age,
                password=password,
                username=random_username
            )
            user.save()

            public_user = PublicUser(user=user, location=location, gender=gender, bio="")
            public_user.save()

            for interest in interest_list:
                user_interest = UserInterests(interest=interest, user=public_user)
                user_interest.save()
            messages.success(request, "User created successfully")
            return redirect("login")
        else:
            context = {
                "form": form
            }
            return render(request, "register.html", context=context)

def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, "login.html", context=context)
    
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                request.session["username"] = user.username
                # login(request, user)
                if user.has_2fa:
                    return redirect("2fa")
                else:
                    return redirect("2fa_enable")
            else:
                messages.error(request, "Invalid email or password")
                context = {
                    "form": form
                }
                return render(request, "login.html", context=context)

def enable_2fa(request):
    if request.method == "GET":
        form = TwoFactorForm()
        username = request.session.get("username")
        qr, token = generate_qr(username)
        context = {
            "qr": qr,
            "token": token,
            "form": form
        }
        return render(request, "enable_2fa.html", context=context)
    elif request.method == "POST":
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            user_token = form.cleaned_data.get("token")
            valid_totp = generate_totp(request.session.get("username"))
            if user_token == valid_totp:
                user = get_user_model().objects.get(username=request.session.get("username"))
                user.has_2fa = True
                user.save()
                messages.success(request, "2FA enabled successfully")
                return redirect("login") # TODO: Redirect to dashboard
            else:
                messages.error(request, "Invalid token")
                context = {
                    "form": form
                }
                return render(request, "enable_2fa.html", context=context)
        else:
            context = {
                "qr": qr,
                "token": token,
                "form": form
            }
            return render(request, "enable_2fa.html", context=context)

def two_factor_view(request):
    if request.method == "GET":
        form = TwoFactorForm()
        context = {
            "form": form
        }
        return render(request, "2fa.html", context=context)
    elif request.method == "POST":
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            user_token = form.cleaned_data.get("token")
            valid_totp = generate_totp(request.session.get("username"))
            if user_token == valid_totp:
                login(request, get_user_model().objects.get(username=request.session.get("username")))
                messages.success(request, "Successfully logged in")
                return redirect("login") # TODO: Redirect to dashboard
            else:
                context = {
                "form": form
            }
            messages.error(request, "Invalid totp")
            return render(request, "2fa.html", context=context)
        else:
            context = {
                "form": form
            }
            messages.error(request, "Invalid data supplied")
            return render(request, "2fa.html", context=context)