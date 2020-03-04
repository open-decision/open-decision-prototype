from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
import os, json
from dashboard.views import build_tree
from dashboard.models import DecisionTree
from django.contrib.auth.decorators import login_required
from builder.forms import NodeFormVisualBuilder
from users.models import Profile


@login_required
def visualbuilder_view(request):
    context = {}
    if os.environ.get('DJANGO_PRODUCTION') is not None:
        context['production'] = True
    #Start interactive tour only the first time the user sees the page
    if request.user.profile.saw_visualbuilder:
         context['start_tour'] = False
    else:
        context['start_tour'] = True
        user_profile = Profile.objects.get(user=request.user)
        user_profile.saw_visualbuilder = True
        user_profile.save(update_fields=['saw_visualbuilder'])
    return render(request, 'visualbuilder.html', context)

def load_node_form(request):
    if request.method == 'GET':
        node_form = NodeFormVisualBuilder
        context = {
        'form': node_form,
        }
        return render(request, 'node_form.html', context)
