from django.shortcuts import render
from pages.models import PublishedTree

def show_interpreter(request):
    context = {'tree_data' : tree.tree_data}
    return render(request, 'publish.html', context)
