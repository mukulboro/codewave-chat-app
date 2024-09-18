from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("enable_2fa/", views.enable_2fa, name="2fa_enable"),
    path("2fa/", views.two_factor_view, name="2fa"),
]