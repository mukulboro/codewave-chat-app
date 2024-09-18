from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    return render(request, "index.html")

def chat(request):
    if request.user.is_authenticated:
        return render(request, "temp_chat.html")
    else:
        messages.error(request, "You need to login first.")
        return redirect("login")
    
def specific_chat(request, chat_id):
    print(chat_id)
    return render(request, "temp_chat.html")

def dashboard(request):
    return render(request, "dashboard.html")