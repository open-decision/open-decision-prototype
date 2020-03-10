from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from users.forms import CustomUserCreationForm
from .models import PublishedTree
import random, string, json
from dashboard.views import build_tree
from dashboard.models import DecisionTree
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    context = {}
    return render(request, 'home.html', context)

def contact_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    context = {}
    return render(request, 'contact.html', context)

def test_view(request, *args, **kwargs):
    context = {}
    return render(request, 'test.html', context)

def handler403(request, exception):
    return render(request, '403.html', status=403)

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

@xframe_options_exempt
def show_published_tree(request, slug):
    if request.GET.get('publish'):
        random_url = publish(request, slug)
        return redirect('/publish/' + random_url + '/?new=true')
    else:
        tree = PublishedTree.objects.get(url=slug)
        context = {'tree_data' : tree.tree_data}
        if request.GET.get('new'):
            context['url'] = slug
        if request.GET.get('embedded'):
            return render(request, 'publish_embedded.html', context)
        return render(request, 'publish.html', context)



@login_required
def publish(request, slug):
    random_url = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    tree_data = json.dumps(build_tree(slug, request), indent=4, default=str)
    t = PublishedTree(  url             = random_url,
                        tree_data       = tree_data,
                        decision_tree   = DecisionTree.objects.filter(owner=request.user).get(slug=slug),
                        owner           = request.user,
                        created_at      = datetime.now(),
                        )
    t.save()
    return random_url

def get_published_tree(request):
    tree_query = request.GET.get('selected_tree')
    tree_data = json.loads(PublishedTree.objects.get(url=tree_query).tree_data)
    return JsonResponse(tree_data, safe=False)
