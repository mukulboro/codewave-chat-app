from django.shortcuts import render, HttpResponse

def test_view(request):
    return HttpResponse("Auther")

# Create your views here.
