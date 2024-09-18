from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="testi"),
    path("chat/",views.chat, name="khai-k-ho-yo"),
    path("chat/<int:chat_id>/", views.specific_chat, name="specific_chat"),
    path("dashboard/",views.dashboard,name="dashboard"),
]