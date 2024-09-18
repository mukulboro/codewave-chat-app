from django.db import models
from auther.models import PublicUser

class Chat(models.Model):
    user1 = models.ForeignKey(PublicUser, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(PublicUser, on_delete=models.CASCADE, related_name='user2')
    blocked = models.BooleanField(default=False)
    u1_name_shown = models.CharField(max_length=100)
    u2_name_shown = models.CharField(max_length=100)
    u1_address_shown = models.CharField(max_length=100)
    u2_address_shown = models.CharField(max_length=100)

class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(PublicUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)