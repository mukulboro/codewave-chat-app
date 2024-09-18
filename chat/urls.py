from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="testi"),
    path("chat/",views.chat, name="chat"),
    path("chat/<int:chat_id>/", views.specific_chat, name="specific_chat"),
]