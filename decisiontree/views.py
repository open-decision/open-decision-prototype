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

@login_required
def node_create_view(request, slug):
    if request.method == 'GET':
        node_form = NodeForm
        NodeButtonFormSet = formset_factory(ButtonAnswersForm)
        context = {
        'form': node_form,
        'selected_tree': DecisionTree.objects.filter(slug=slug).values()[0]
        }
        return render(request, 'node_create.html', context)
    elif request.method == 'POST' and request.POST.get('save'):
        save_node(request, slug)
        return redirect('/trees/'+str(slug)+'/')

@login_required
def node_edit_view(request, slug, node_slug):
    data_node = Node.objects.get(slug=node_slug)
    input_type = data_node.input_type
    node_form = NodeForm({'name': data_node.name, 'question': data_node.question, 'input_type': data_node.input_type})
    answer_form = load_answer_field(request, input_type, data_node)
    context = {
        'form': node_form,
        'selected_tree': DecisionTree.objects.filter(slug=slug).values()[0],
        'edit': 'true'
        }
    return render(request, 'node_create.html', context)


@login_required
def load_answer_field(request, *args):
    input_type = request.GET['input_type']
    list = set_answer_form(input_type)
    answer_form = list[0]
    expandable = list[1]
    AnswerFormSet = formset_factory(answer_form)
    answer_formset = AnswerFormSet(prefix='answer')
    context = {
    'answer_formset': answer_formset,
    'expandable': expandable,
    }
    return render(request, 'answer_field.html', context)
'''    try:
        input_type = args[0]
        data_node = args[1]
    except:
        pass
    if input_type:
        list = set_answer_form(input_type)
        answer_form = list[0]
        expandable = list[1]
        data = json.loads(data_node.data_answer)
        AnswerFormSet = formset_factory(answer_form)
        answer_formset = AnswerFormSet(initial=data, prefix='answer')
        context = {
        'answer_formset': answer_formset,
        'expandable': expandable,
        }
        return render(request, 'answer_field.html', context)
    else:
        '''

def set_answer_form(input_type):
    if input_type == 'button':
        answer_form = ButtonAnswersForm
        expandable = True
    elif input_type == 'list':
        answer_form = ListAnswersForms
        expandable = False
    elif input_type == 'multiple_select':
        answer_form = MultipleSelectAnswersForm
        expandable = True
    elif input_type == 'short_text':
        answer_form = ShortTextAnswersForm
        expandable = True
    elif input_type == 'long_text':
        answer_form = LongTextAnswersForm
        expandable = True
    elif input_type == 'number':
        answer_form = NumberAnswersForm
        expandable = False
    elif input_type == 'date':
        answer_form = DateAnswerForm
        expandable = False
    else:
        raise Exception('Invalid input type.')
    return [answer_form, expandable]

@login_required
def load_logic_field(request):
    input_type = request.GET['input_type']
    LogicFormSet = formset_factory(LogicForm)

    if input_type == 'button':
        logic_form = LogicFormSet(form_kwargs={'input_type': input_type}, prefix='logic')
    elif input_type == 'list':
        logic_form = LogicFormSet(form_kwargs={'input_type': input_type}, prefix='logic')
    elif input_type == 'multiple_select':
        logic_form = LogicFormSet(form_kwargs={'action': '', 'input_type': input_type}, prefix='logic')
    elif input_type == 'short_text':
        logic_form = LogicFormSet(form_kwargs={'action': '', 'input_type': input_type}, prefix='logic')
    elif input_type == 'long_text':
        logic_form = LogicFormSet(form_kwargs={'action': '', 'input_type': input_type}, prefix='logic')
    elif input_type == 'number':
        logic_form = LogicFormSet(form_kwargs={'action': '', 'input_type': input_type}, prefix='logic')
    elif input_type == 'date':
        logic_form = LogicFormSet(form_kwargs={'action': '', 'input_type': input_type}, prefix='logic')
    else:
        raise Exception('Invalid input type.')
    context = {
    'logic': logic_form
    }
    return render(request, 'logic_field.html', context)

@login_required
def load_nodes(request):
    selected_tree = request.GET['selected_tree']
    data_all = Node.objects.filter(decision_tree__slug=selected_tree).values()
    data = []
    for item in data_all:
        data.append({"label" : item["name"], "value" : item['slug']})
    response = JsonResponse(data, safe=False)
    return response

@login_required
def save_node(request, slug):
#ToDo: Process errors properly -  build error dict, display to user
    node_dirty = {
            'name'      : request.POST.get('name'),
            'question'  : request.POST.get('question'),
            'input_type': request.POST.get('input_type'),
            }
#Clean node data, TODO unify naming/syntax with logic and answers
    node_form = NodeForm(node_dirty)
    if node_form.is_valid():
        node_clean = node_form.cleaned_data
#Clean answer data
    data_answer = []
    data_answer_dirty = {
    'answer-TOTAL_FORMS'  : request.POST.get('answer-TOTAL_FORMS'),
    'answer-INITIAL_FORMS': request.POST.get('answer-INITIAL_FORMS'),
    'answer-MIN_NUM_FORMS': request.POST.get('answer-MIN_NUM_FORMS'),
    'answer-MAX_NUM_FORMS': request.POST.get('answer-MAX_NUM_FORMS')
    }
    for i in range(int(data_answer_dirty['answer-TOTAL_FORMS'])):
        data_answer_dirty['answer-'+ str(i) +'-answer'] = request.POST.get('answer-'+ str(i) +'-answer')
#Perform Logic Formset Validation
    AnswerFormUsed = set_answer_form(node_clean['input_type'])[0]
    AnswerFormSet = formset_factory(AnswerFormUsed)
    answer_form_instance = AnswerFormSet(data_answer_dirty, prefix='answer')
    if answer_form_instance.is_valid():
        data_answer = answer_form_instance.cleaned_data
#Clean Logic data
#Build data logic dirty form
    data_logic = []
    data_logic_dirty = {
    'logic-TOTAL_FORMS'  : request.POST.get('logic-TOTAL_FORMS'),
    'logic-INITIAL_FORMS': request.POST.get('logic-INITIAL_FORMS'),
    'logic-MIN_NUM_FORMS': request.POST.get('logic-MIN_NUM_FORMS'),
    'logic-MAX_NUM_FORMS': request.POST.get('logic-MAX_NUM_FORMS')
    }
    for i in range(int(data_logic_dirty['logic-TOTAL_FORMS'])):
        data_logic_dirty['logic-'+ str(i) +'-operator'] = request.POST.get('logic-'+ str(i) +'-operator')
        data_logic_dirty['logic-'+ str(i) +'-answers_logic'] = request.POST.get('logic-'+ str(i) +'-answers_logic')
        data_logic_dirty['logic-'+ str(i) +'-action'] = request.POST.get('logic-'+ str(i) +'-action')
        data_logic_dirty['logic-'+ str(i) +'-var_to_modify'] = request.POST.get('logic-'+ str(i) +'-var_to_modify')
#Perform Logic Formset Validation
    LogicFormSet = formset_factory(LogicForm)
    logic_form_instance = LogicFormSet(data_logic_dirty, form_kwargs={'input_type': node_clean['input_type']}, prefix='logic')
    if logic_form_instance.is_valid():
        data_logic= logic_form_instance.cleaned_data
#Check if connected nodes already exist
    for i in range(len(data_logic)):
        try:
            #If yes, get ID to avoid issues if connected node is renamed
            id= Node.objects.get(slug=slugify(data_logic[i]['var_to_modify'])).id
            data_logic[i]['var_to_modify'] = id
        except:
            #If not, create new node
            new = Node(name= data_logic[i]['var_to_modify'],
            slug= slugify(data_logic[i]['var_to_modify']),
            decision_tree= DecisionTree.objects.get(slug=slug),
                    )
            new.save()
            data_logic[i]['var_to_modify'] = new.id
#Save the node, TODO: change to JSON field for saving answer and logic
    n = Node(name= node_clean['name'],
        slug= slugify(node_clean['name']),
        decision_tree= DecisionTree.objects.get(slug=slug),
        question= node_form.cleaned_data['question'],
        input_type= node_form.cleaned_data['input_type'],
        data_answer= json.dumps(data_answer),
        data_logic= json.dumps(data_logic),
        )
    n.save()

def export(request):
#0. Check for errors - how?
#1. Build header
#2. 
    pass
