from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Chat, ChatMessage
from auther.models import PublicUser
from .utils import FiboCaeser

def index(request):
    return render(request, "index.html")

def chat(request):
    if request.user.is_authenticated:
        return render(request, "chatdash.html")
    else:
        messages.error(request, "You need to login first.")
        return redirect("login")
    
def specific_chat(request, chat_id):

    chat = Chat.objects.get(id=chat_id)
    if request.user != chat.user1.user and request.user != chat.user2.user:
        messages.error(request, "You are not authorized to view this chat.")
        return redirect("dashboard")
    them = chat.user2 if chat.user1.user.pk == request.user.pk else chat.user1
    encryptor = FiboCaeser(them.user.pk, chat.pk)
    their_encrypted_name = encryptor.encrypt(f"{them.user.first_name} {them.user.last_name}")
    their_encrypted_location = encryptor.encrypt(them.location)
    location_decryption_pattern = chat.u2_address_shown if chat.user1.user.pk == request.user.pk else chat.u1_address_shown
    decryption_pattern = chat.u2_name_shown if chat.user1.user.pk == request.user.pk else chat.u1_name_shown
    their_decrypted_name = encryptor.decrypt(their_encrypted_name, decryption_pattern)
    their_decrypted_location = encryptor.decrypt(their_encrypted_location, location_decryption_pattern)

    my_name_pattern = chat.u1_name_shown if chat.user1.user.pk == request.user.pk else chat.u2_name_shown
    my_location_pattern = chat.u1_address_shown if chat.user1.user.pk == request.user.pk else chat.u2_address_shown
    my_name = list(request.user.first_name + " " + request.user.last_name)
    my_location = list(PublicUser.objects.get(user=request.user).location)

    for i, chr in enumerate(my_name):
        if my_name_pattern[i] == '0':
            my_name[i] = "_"
    for i, chr in enumerate(my_location):
        if my_location_pattern[i] == '0':
            my_location[i] = "_"

    my_chats = Chat.objects.filter(user1__user=request.user) | Chat.objects.filter(user2__user=request.user)
    filtered_chats = []

    for chat in my_chats:
        messages = ChatMessage.objects.filter(chat=chat).order_by("-timestamp")
        last_message = messages[0] if messages else None
        if chat.user1.user.pk == request.user.pk:
            filtered_chats.append({
                "chat_id": chat.pk,
                "their_username": chat.user2.user.username[0:10],
                "last_message": (last_message.message.strip())[0:12] if last_message else "No messages yet",
            })
        else:
            filtered_chats.append({
                "chat_id": chat.pk,
                "their_username": chat.user1.user.username[0:10],
                "last_message": (last_message.message.strip())[0:12] if last_message else "No messages yet",
            })
    context = {
        "their_encrypted_name": their_decrypted_name,
        "their_encrypted_location": their_decrypted_location,
        "my_name_pattern": "".join(my_name),
        "my_location_pattern": "".join(my_location),
        "messages": ChatMessage.objects.filter(chat=chat),
        "chat_id": chat_id,
        "current_user": request.user.username,
        "my_chats": filtered_chats,
    }
    return render(request, "chatdash.html", context=context)

def dashboard(request):
    return render(request, "dashboard.html")
