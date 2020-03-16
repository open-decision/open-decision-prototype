from django.shortcuts import render, redirect
from .forms import *
from django.forms import formset_factory
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from dashboard.models import DecisionTree, Node
from django.utils.text import slugify
import json
from django.template.loader import render_to_string
from dashboard.models import bleach_clean


@login_required
def node_create_view(request, slug):
    if request.method == 'GET':
        node_form = NodeForm
        context = {
        'form': node_form,
        'selected_tree': DecisionTree.objects.filter(owner=request.user).filter(slug=slug).values()[0],
        }
        return render(request, 'node_create.html', context)
    elif request.method == 'POST' and request.POST.get('save'):
        save_node(request, slug)
        return redirect('/trees/'+str(slug)+'/')

@login_required
def node_edit_view(request, slug, node_slug):
    if request.method == 'GET':
        data_node = Node.objects.filter(decision_tree__owner=request.user).get(slug=node_slug)
        node_form = NodeForm({'name': data_node.name, 'question': data_node.question})

        logic_formset_init = load_logic_module(request, input_type, data_node)
        context = {
            'form': node_form,
            'selected_tree': DecisionTree.objects.filter(owner=request.user).filter(slug=slug).values()[0],
            'answer_formset_init': answer_formset_init,
            'logic_formset_init': logic_formset_init,
            'edit': 'true',
            }
        return render(request, 'node_create.html', context)

    elif request.method == 'POST' and request.POST.get('save'):
            id = Node.objects.filter(decision_tree__owner=request.user).get(slug=node_slug).id
            save_node(request, slug, id)
            return redirect('/trees/'+str(slug)+'/')

@login_required
def load_token(request):
    selected_tree = request.GET.get('selected_tree')
    data = [[n.name, n.slug] for n in Node.objects.filter(decision_tree__owner=request.user).filter(decision_tree__slug=selected_tree)]
    return JsonResponse(data, safe=False)


@login_required
def load_input_form(request, *args):
    try:
# This will fail, if the fct is not called by the edit view
            input_type = args[0]
            data_node = args[1]
    except:
        input_type = False
# If called by edit view
    if input_type:
        inputForm
        data = json.loads(data_node.data_answer)
        AnswerFormSet = formset_factory(InputForm, extra=0)
        answer_formset_init = AnswerFormSet(initial=data, prefix='answer')
        context = {
            'answer_formset_init': answer_formset_init,
            'expandable': True if input_type=='button' else False,
            'edit': 'true',
            }
        rendered = render_to_string('answer_field.html', context)
        return rendered
# If called by ajax when creating new node
    else:
        input_type = request.GET.get('input_type', 'button')
        print(input_type)
        InputFormSet = formset_factory(InputForm)
        context = {
        'input_formset': InputFormSet(form_kwargs={'input_type': input_type}, prefix='input'),
        'expandable': True if (input_type=='button' or input_type == 'short_text') else False,
        }
        return render(request, 'input_form.html', context)


@login_required
def load_logic_module(request, *args):
    try:
# This will fail, if the fct is not called by the edit view
        input_type = args[0]
        data_node = args[1]
    except:
        input_type = False
# If called by edit view
    if input_type:
        data = json.loads(data_node.data_logic)
        for logic_form in data:
            if logic_form['target'] != '':
                try:
                    node_slug= Node.objects.filter(decision_tree__owner=request.user).get(id=logic_form['target']).slug
                except:
                    node_slug = ''
                logic_form['target']= node_slug
        LogicFormSet = formset_factory(LogicForm, extra=0)
        logic_formset_init = LogicFormSet(initial=data, form_kwargs={'input_type': input_type}, prefix='logic')
        context = {
        'logic_formset_init': logic_formset_init,
        'edit': 'true',
        }
        rendered = render_to_string('logic_module.html', context)
        return rendered
# If called by ajax when creating new node
    else:
        input_type = request.GET['input_type']
        LogicFormSet = formset_factory(LogicForm)
        logic_formset = LogicFormSet(form_kwargs={'input_type': input_type}, prefix='logic')
        context = {
        'logic_formset': logic_formset
        }
        if request.GET.get('visualbuilder'):
            context['visualbuilder'] = True
        return render(request, 'logic_module.html', context)

@login_required
def load_nodes(request):
    selected_tree = request.GET['selected_tree']
    data_all = Node.objects.filter(decision_tree__owner=request.user).filter(decision_tree__slug=selected_tree).values()
    data = []
    for item in data_all:
        data.append({'label' : item['name'], 'value' : item['slug']})
    response = JsonResponse(data, safe=False)
    return response

@login_required
def save_node(request, slug, *args):
#ToDo: Process errors properly -  build error dict, display to user
    print(request.POST)
    node_dirty = {
            'name'      : request.POST.get('name'),
            'question'  : request.POST.get('question'),
            }
#Clean node data, TODO unify naming/syntax with logic and answers
    node_form = NodeForm(node_dirty)
    if node_form.is_valid():
        node_clean = node_form.cleaned_data
#Clean input data
    data_input_dirty = {}
    data_input = []
    for key, value in request.POST.items():
        if key.startswith('input-'):
            data_input_dirty[key] = value
#Perform Logic Formset Validation
    InputFormSet = formset_factory(InputForm)
    Input_form_instance = InputFormSet(data_input_dirty, form_kwargs={'input_type': request.POST.get('input-0-input_type')}, prefix='input')
    if Input_form_instance.is_valid():
        data_input = Input_form_instance.cleaned_data
        if data_input[0]['input_type'] == 'short_text':
            data_input[0]['destination'] = bleach_clean(request.POST.get('short-text-destination'))
    print(data_input)
#Clean Logic data
#Build data logic dirty form
    data_logic = []
    data_logic_dirty = {}
    for key, value in request.POST.items():
        if key.startswith('logic-'):
            data_logic_dirty[key] = value
#Perform Logic Formset Validation
    if len(data_logic_dirty) != 0:
        LogicFormSet = formset_factory(LogicForm)
        logic_form_instance = LogicFormSet(data_logic_dirty, form_kwargs={'input_type': request.POST.get('input-0-input_type')}, prefix='logic')
        if logic_form_instance.is_valid():
            data_logic= logic_form_instance.cleaned_data

#Perform input and logic matching, currently not necessary

#Check if connected nodes already exist
    is_start_node = False if Node.objects.filter(decision_tree__owner=request.user).filter(decision_tree__slug=slug) else True
    for i in range(len(data_logic)):
        if data_logic[i]['target'] != '':
            try:
                #If yes, get ID to avoid issues if connected node is renamed
                id= Node.objects.filter(decision_tree__owner=request.user).get(slug=slugify(data_logic[i]['target'])).id
                data_logic[i]['target'] = id
            except:
                #If not, create new node
                new = Node(name= data_logic[i]['target'],
                slug= slugify(data_logic[i]['target']),
                decision_tree= DecisionTree.objects.filter(owner=request.user).get(slug=slug),
                input_type= 'button',
                data_answer= json.dumps([]),
                data_logic= json.dumps([]),
                new_node= True,
                start_node= False,
                end_node= False,
                        )
                new.save()
                data_logic[i]['target'] = new.id
#Save the node, todo: change to JSON field for saving answer and logic
    try:
        id = args[0]
    except:
        id = False
    is_end_node = True if  node_form.cleaned_data['input_type'] == 'end_node' else False
    if id:
        Node.objects.filter(id=id).update(
        name= node_clean['name'],
            slug= slugify(node_clean['name']),
            decision_tree= DecisionTree.objects.filter(owner=request.user).get(slug=slug),
            question= node_form.cleaned_data['question'],
            input_type= node_form.cleaned_data['input_type'],
            data_answer= json.dumps(data_answer),
            data_logic= json.dumps(data_logic),
            new_node= False,
            end_node= is_end_node,
        )
    else:
        n = Node(name= node_clean['name'],
        slug= slugify(node_clean['name']),
        decision_tree= DecisionTree.objects.filter(owner=request.user).get(slug=slug),
        question= node_form.cleaned_data['question'],
        input_type= node_form.cleaned_data['input_type'],
        data_answer= json.dumps(data_answer),
        data_logic= json.dumps(data_logic),
        new_node= False,
        start_node= is_start_node,
        end_node= is_end_node,
        )
        n.save()
