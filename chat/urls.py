from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="testi"),
    path("chat/",views.chat, name="chat"),
    path("chat/<int:chat_id>/", views.specific_chat, name="specific_chat"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("dashboard/<int:user_id>/",views.create_new_chat,name="create_new_chat"),
    path("settings/", views.settings,name="settings"),
]