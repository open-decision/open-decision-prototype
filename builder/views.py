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
from django.db import IntegrityError
from django.utils.translation import gettext as _
from django.contrib import messages

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
        result = save_node(request, slug)
        if True: #result == True:
            return redirect('/trees/'+str(slug)+'/')
        else:
             messages.error(request, "Error")
        #return render(request, 'node_create.html', context)
@login_required
def node_edit_view(request, slug, node_slug):
    if request.method == 'GET':
        data_node = Node.objects.filter(decision_tree__owner=request.user).get(slug=node_slug)
        node_form = NodeForm({'name': data_node.name, 'question': data_node.question})

        try:
            input_type = json.loads(data_node.inputs)[0]['input_type']
        except (KeyError, IndexError):
            input_type = 'button'
        if input_type not in ['button','short_text', 'end_node']:
            data_input = json.loads(data_node.inputs)
            data_logic = data_input.pop()
            logic_formset_init = load_logic_module(request, input_type, data_logic)
        else:
            data_input = json.loads(data_node.inputs)
            logic_formset_init = None

        short_text_destination = json.loads(data_node.inputs)[0].pop('destination', '') if input_type == 'short_text' else None
        input_formset_init = load_input_form(request, input_type, data_input, logic_formset_init)
        context = {
            'form': node_form,
            'selected_tree': DecisionTree.objects.filter(owner=request.user).filter(slug=slug).values()[0],
            'input_formset_init': input_formset_init,
            'edit': True,
            'short_text_destination': short_text_destination,
            'input_type': input_type,
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
        data_input = args[1]
        logic_formset_init = args[2]
    except:
        data_input = False
# If called by edit view
    if data_input:
        for form in data_input:
            if 'target' in form and form['target'] != '':
                dest_key = 'target'
            elif 'destination' in form and form['destination'] != '':
                dest_key = 'destination'
            else:
                dest_key = False
            if dest_key:
                try:
                    node_slug= Node.objects.filter(decision_tree__owner=request.user).get(id=form[dest_key]).slug
                except:
                    node_slug = ''
                form[dest_key]= node_slug
        InputFormSet = formset_factory(InputForm, extra=0)
        input_formset_init = InputFormSet(initial=data_input, form_kwargs={'input_type': input_type}, prefix='input')
        context = {
            'input_formset_init': input_formset_init,
            'expandable': True if (input_type=='button' or input_type == 'short_text') else False,
            'edit': True,
            }
        if logic_formset_init:
            context['logic_formset_init'] = logic_formset_init
        rendered = render_to_string('input_form.html', context)
        return rendered
# If called by ajax when creating new node
    else:
        input_type = request.GET.get('input_type', 'button')
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
        data_logic = args[1]
    except:
        data_logic = False
# If called by edit view
    if data_logic:
        for form in data_logic:
            if 'target' in form and form['target'] != '':
                dest_key = 'target'
            elif 'destination' in form and form['destination'] != '':
                dest_key = 'destination'
            else:
                dest_key = False
            if dest_key:
                try:
                    node_slug= Node.objects.filter(decision_tree__owner=request.user).get(id=form[dest_key]).slug
                except:
                    node_slug = ''
                form[dest_key]= node_slug
        LogicFormSet = formset_factory(LogicForm, extra=0)
        logic_formset_init = LogicFormSet(initial=data_logic, form_kwargs={'input_type': input_type}, prefix='logic')
        context = {
        'logic_formset_init': logic_formset_init,
        'edit': 'True',
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
#Save data from request
    data_input_dirty = {}
    data_input = []
    data_logic_dirty = {}
    data_logic = []

    for key, value in request.POST.items():
        if key.startswith('input-'):
            data_input_dirty[key] = value
        if key.startswith('logic-'):
            data_logic_dirty[key] = value
#Perform Logic Formset Validation
    InputFormSet = formset_factory(InputForm)
    Input_form_instance = InputFormSet(data_input_dirty, form_kwargs={'input_type': request.POST.get('input-0-input_type')}, prefix='input')
    if Input_form_instance.is_valid():
        data_input = Input_form_instance.cleaned_data
    else:
        print(Input_form_instance.errors)

    if data_input and (data_input[0]['input_type'] == 'short_text'):
        data_input[0]['destination'] = bleach_clean(request.POST.get('short-text-destination'))
    print(data_input)
#Clean Logic data
#Perform Logic Formset Validation
    if len(data_logic_dirty) != 0:
        LogicFormSet = formset_factory(LogicForm)
        logic_form_instance = LogicFormSet(data_logic_dirty, form_kwargs={'input_type': request.POST.get('input-0-input_type')}, prefix='logic')
        if logic_form_instance.is_valid():
            data_logic= logic_form_instance.cleaned_data

    is_end_node = True if (data_input and (data_input[0]['input_type'])) == 'end_node' else False

#Perform input and logic matching, currently not necessary
# atm not necessary, only append logic to input data
    if len(data_logic) != 0:
        data_input.append(data_logic)
#Check if connected nodes already exist
    is_start_node = False if Node.objects.filter(decision_tree__owner=request.user).filter(decision_tree__slug=slug) else True
    print(data_input)
    dest_key= False
    for i in range(len(data_input)):
        if 'target' in data_input[i]:
            if data_input[i]['target'] != '':
                dest_key = 'target'
        elif 'destination' in data_input[i]:
            if data_input[i]['destination'] != '':
                dest_key = 'destination'
        if dest_key:
            try:
                #If yes, get ID to avoid issues if connected node is renamed
                id= Node.objects.filter(decision_tree__owner=request.user).get(slug=slugify(data_input[i][dest_key])).id
                data_input[i][dest_key] = id
                dest_key = False
            except:
                #If not, create new node
                new = Node(
                name= data_input[i][dest_key],
                slug= slugify(data_input[i][dest_key]),
                decision_tree= DecisionTree.objects.filter(owner=request.user).get(slug=slug),
                #path= json.dumps([]),
                inputs= json.dumps([{}]),
                new_node= True,
                start_node= False,
                end_node= False,
                        )
                new.save()
                data_input[i][dest_key] = new.id
                dest_key = False
#Save the node, todo: change to postgres JSON field
    try:
        id = args[0]
    except:
        id = False
    if id:
        Node.objects.filter(id=id).update(
            name= node_clean['name'],
            slug= slugify(node_clean['name']),
            decision_tree= DecisionTree.objects.filter(owner=request.user).get(slug=slug),
            #path =  json.dumps([] if not is_start_node else []),
            question= node_form.cleaned_data['question'],
            inputs= json.dumps(data_input),
            new_node= False,
            end_node= is_end_node,
        )
        return True
    else:
        try:
            n = Node(
            name= node_clean['name'],
            slug= slugify(node_clean['name']),
            decision_tree= DecisionTree.objects.filter(owner=request.user).get(slug=slug),
            #path =  json.dumps([] if not is_start_node else []),
            question= node_form.cleaned_data['question'],
            inputs= json.dumps(data_input),
            new_node= False,
            start_node= is_start_node,
            end_node= is_end_node,
            )
            n.save()
            return True
        except IntegrityError:
            return '<div class="border-left-danger pl-2">'+ _('<p>Please choose another name, you already have a node with this name.</p>') + '</div>'
