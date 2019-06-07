from django.shortcuts import render, redirect
from django.views import generic
from .models import DecisionTree, Node
from .forms import DecisionTreeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

@login_required
def dashboard_view(request):
    if request.method == 'GET':
        form = DecisionTreeForm()
        context = {
         'decisiontree_list': DecisionTree.objects.filter(owner=request.user),
         'form':form,
         }
    return render(request, 'dashboard.html', context)

@login_required
def add_tree(request):
    f = DecisionTreeForm(request.POST)
    if f.is_valid():
        tree = f.save(commit=False)
        tree.owner = request.user
        tree.save()
    context = {
     'decisiontree_list': DecisionTree.objects.filter(owner=request.user)
     }
    return render(request, 'decisiontree_list.html', context)

@login_required
def tree_view(request, slug):
    existing_nodes = Node.objects.filter(decision_tree__slug=slug).filter(new_node=False)
    new_nodes = Node.objects.filter(decision_tree__slug=slug).filter(new_node=True)
    if request.method == 'GET':
        context = {
        'existing_nodes': existing_nodes,
         'new_nodes': new_nodes,
         'selected_tree': DecisionTree.objects.filter(slug=slug).values()[0]
         }
    return render(request, 'tree_view.html', context)
