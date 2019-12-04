from django.shortcuts import render, redirect
from django.http import HttpResponse


# Create your views here.
def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    context = {}
    return render(request, 'home.html', context)

def contact_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    context = {}
    return render(request, 'contact.html', context)

def test_view(request, *args, **kwargs):
    context = {}
    return render(request, 'test.html', context)

def register_user(request):
    context = {}
    return render(request, 'registration/register.html', context)
