from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Chat, ChatMessage
from auther.models import PublicUser, UserInterests
from .utils import FiboCaeser, similarity_score

def index(request):
    return render(request, "index.html")

def chat(request):
    if request.user.is_authenticated:
        my_chats = Chat.objects.filter(user1__user=request.user) | Chat.objects.filter(user2__user=request.user)
        one_chat = my_chats.first().pk
        return redirect("specific_chat", one_chat)
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

    profile_picture = None

    for i, chr in enumerate(my_name):
        if my_name_pattern[i] == '0':
            my_name[i] = "_"
    for i, chr in enumerate(my_location):
        if my_location_pattern[i] == '0':
            my_location[i] = "_"

    if '0' not in decryption_pattern and '0' not in location_decryption_pattern:
        profile_picture = them.profile_picture

    my_chats = Chat.objects.filter(user1__user=request.user) | Chat.objects.filter(user2__user=request.user)
    filtered_chats = []

    for chat in my_chats:
        messages = ChatMessage.objects.filter(chat=chat).order_by("-timestamp")
        last_message = messages[0] if messages else None
        if chat.user1.user.pk == request.user.pk:
            filtered_chats.append({
                "chat_id": chat.pk,
                "their_username": chat.user2.user.username[0:10],
                "their_profile_picture": profile_picture.url if profile_picture else None,
                "last_message": (last_message.message.strip())[0:12] if last_message else "No messages yet",
            })
        else:
            filtered_chats.append({
                "chat_id": chat.pk,
                "their_username": chat.user1.user.username[0:10],
                "their_profile_picture": profile_picture.url if profile_picture else None,
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
     if request.user.is_authenticated:
        full_name = request.user.first_name + " " + request.user.last_name
        current_public_user = PublicUser.objects.get(user=request.user)
        all_users = PublicUser.objects.all()
        filtered_users = []
        for users in all_users:
            existing_chats_user_ids = set(Chat.objects.filter(user1__user=request.user).values_list('user2__user__id', flat=True)) | set(Chat.objects.filter(user2__user=request.user).values_list('user1__user__id', flat=True))
            if users.user.id in existing_chats_user_ids:
                continue
            if not users.user == request.user:
                similarity = similarity_score(UserInterests.objects.filter(user=current_public_user).values_list("interest", flat=True), UserInterests.objects.filter(user=users).values_list("interest", flat=True))
                user_interests = UserInterests.objects.filter(user=users).values_list("interest", flat=True)
                filtered_users.append({
                    "user": users,
                    "interests": [str(i).upper() for i in user_interests],
                    "similarity": similarity
                })
        filtered_users.sort(key=lambda x: x["similarity"], reverse=True)

        context = {
            "full_name": full_name,
            "filtered_users": filtered_users
        }
        return render(request, "dashboard.html", context=context)
     else:
        messages.error(request, "You need to login first.")
        return redirect("login")

def create_new_chat(request, user_id):
    if request.user.is_authenticated:
        user2 = PublicUser.objects.get(user__pk=user_id)
        user2_full_name = user2.user.first_name + " " + user2.user.last_name
        user1_full_name = request.user.first_name + " " + request.user.last_name

        user2_location = user2.location
        user1_location = PublicUser.objects.get(user=request.user).location

        user1_location_pattern = ["0" for _ in range(len(user1_location))]
        user2_location_pattern = ["0" for _ in range(len(user2_location))]

        user2_pattern = ["0" for _ in range(len(user2_full_name))]
        user1_pattern = ["0" for _ in range(len(user1_full_name))]
    
        chat = Chat.objects.create(user1=PublicUser.objects.get(user=request.user), 
                                   user2=user2, u1_name_shown="".join(user1_pattern), 
                                   u2_name_shown="".join(user2_pattern), 
                                   u1_address_shown="".join(user1_location_pattern), 
                                   u2_address_shown="".join(user2_location_pattern))
        chat.save()
        return redirect("specific_chat", chat.pk)
    else:
        messages.error(request, "You need to login first.")
        return redirect("login")