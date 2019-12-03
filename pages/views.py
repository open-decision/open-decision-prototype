from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, 'home.html', {})

def contact_view(request, *args, **kwargs):
    my_context = {
    }
    return render(request, 'contact.html', my_context)

def test_view(request, *args, **kwargs):
    context = {}
    return render(request, 'test.html', context)

    
