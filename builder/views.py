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
    if request.method == 'GET':
        data_node = Node.objects.get(slug=node_slug)
        input_type = data_node.input_type
        if input_type == '':
            input_type = 'button'
        node_form = NodeForm({'name': data_node.name, 'question': data_node.question, 'input_type': data_node.input_type})
        answer_formset_init = load_answer_field(request, input_type, data_node)
        logic_formset_init = load_logic_field(request, input_type, data_node)
        context = {
            'form': node_form,
            'selected_tree': DecisionTree.objects.filter(slug=slug).values()[0],
            'answer_formset_init': answer_formset_init,
            'logic_formset_init': logic_formset_init,
            'edit': 'true',
            }
        return render(request, 'node_create.html', context)
    elif request.method == 'POST' and request.POST.get('save'):
            id = Node.objects.get(slug=node_slug).id
            save_node(request, slug, id)
            return redirect('/trees/'+str(slug)+'/')


@login_required
def load_answer_field(request, *args):
    try:
# This will fail, if the fct is not called by the edit view
            input_type = args[0]
            data_node = args[1]
    except:
        input_type = False
# If called by edit view
    if input_type:
        list = set_answer_form(input_type)
        answer_form = list[0]
        expandable = list[1]
        data = json.loads(data_node.data_answer)
        AnswerFormSet = formset_factory(answer_form, extra=0)
        answer_formset_init = AnswerFormSet(initial=data, prefix='answer')
        context = {
            'answer_formset_init': answer_formset_init,
            'expandable': expandable,
            'edit': 'true',
            }
        rendered = render_to_string('answer_field.html', context)
        return rendered
# If called by ajax when creating new node
    else:
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
    elif input_type == 'end_node':
        answer_form = EndNodeAnswerForm
        expandable = False
    else:
        raise Exception('Invalid input type.')
    return [answer_form, expandable]

@login_required
def load_logic_field(request, *args):
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
            if logic_form['var_to_modify'] != '':
                try:
                    node_slug= Node.objects.get(id=logic_form['var_to_modify']).slug
                except:
                    node_slug = ''
                logic_form['var_to_modify']= node_slug
        LogicFormSet = formset_factory(LogicForm, extra=0)
        logic_formset_init = LogicFormSet(initial=data, form_kwargs={'input_type': input_type}, prefix='logic')
        context = {
        'logic_formset_init': logic_formset_init,
        'edit': 'true',
        }
        rendered = render_to_string('logic_field.html', context)
        return rendered
# If called by ajax when creating new node
    else:
        input_type = request.GET['input_type']
        LogicFormSet = formset_factory(LogicForm)
        logic_formset = LogicFormSet(form_kwargs={'input_type': input_type}, prefix='logic')
        context = {
        'logic_formset': logic_formset
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
def save_node(request, slug, *args):
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
        if data_logic[i]['var_to_modify'] != '':
            try:
                #If yes, get ID to avoid issues if connected node is renamed
                id= Node.objects.get(slug=slugify(data_logic[i]['var_to_modify'])).id
                data_logic[i]['var_to_modify'] = id
            except:
                #If not, create new node
                new = Node(name= data_logic[i]['var_to_modify'],
                slug= slugify(data_logic[i]['var_to_modify']),
                decision_tree= DecisionTree.objects.get(slug=slug),
                input_type= 'button',
                data_answer= json.dumps([]),
                data_logic= json.dumps([]),
                new_node= True,
                start_node= False,
                        )
                new.save()
                data_logic[i]['var_to_modify'] = new.id
#Save the node, TODO: change to JSON field for saving answer and logic
    try:
        id = args[0]
    except:
        id = False
    if id:
        Node.objects.filter(id=id).update(
        name= node_clean['name'],
            slug= slugify(node_clean['name']),
            decision_tree= DecisionTree.objects.get(slug=slug),
            question= node_form.cleaned_data['question'],
            input_type= node_form.cleaned_data['input_type'],
            data_answer= json.dumps(data_answer),
            data_logic= json.dumps(data_logic),
            new_node= False
        )
    else:
        n = Node(name= node_clean['name'],
        slug= slugify(node_clean['name']),
        decision_tree= DecisionTree.objects.get(slug=slug),
        question= node_form.cleaned_data['question'],
        input_type= node_form.cleaned_data['input_type'],
        data_answer= json.dumps(data_answer),
        data_logic= json.dumps(data_logic),
        new_node= False,
        start_node= False,
        )
        n.save()

@login_required
def export_tree(request, slug):
    context = {}
#0. Check for errors - how?
#1. Build header
#2.
    check_tree(slug)
    pass
    #return render(request, 'export.html', context)


def check_tree(slug):
    #Build dic with tree structure to check tree integrity


# if data_answer or data_logic empty AND not end_node
# are answers matching? buttons -> make field not editable; how to check others?

    tree_name=slug
    all = Node.objects.filter(decision_tree__slug=slug)
    end_nodes = all.filter(end_node=True)
    no_end_nodes = all.filter(end_node=False)

# Build errors dict for nodes without data_answer or data_logic
    errors = {
        'no_answers': [n.id for n in no_end_nodes.filter(data_answer='[]')],
        'no_logic': [n.id for n in no_end_nodes.filter(data_logic='[]')],
        'no_var':{},
        'no_ref_to_start':{},
        'no_ref_to_end':{},
        }
    paths = {'node_list':[], 'start_node': all.get(start_node=True).id, 'end_nodes':[], 'nodes':{}}
    for n in all:
        paths['node_list'].append(n.id)
        paths['nodes'][n.id]=[]
        l = []
        for d in json.loads(n.data_logic):
            if d['action'] == 'go_to':
                if d['var_to_modify'] == "":
        #Ist das hier noch relevant? -> ja, weil in Logic auch daten ohne
                    errors['no_var'][n.id] = d['answers_logic']
                else:
                    l.append(d['var_to_modify'])
        paths['nodes'][n.id] = l
    paths['end_nodes'] = [e.id for e in end_nodes]
    single_paths = build_paths(paths)
    print(single_paths)

def build_paths(paths):
    num_of_childs_left = []
    single_paths= []
    if paths['nodes'][paths['start_node']] is None:
        return #some Error saying start is not connected
    return iterator(paths, num_of_childs_left, single_paths, 0)

def iterator(paths, num_of_childs_left, single_paths, last_fork):
# builds one full path and is then called again
    temp_path = []
# In first run
    if len(single_paths) == 0:
        node = paths['start_node']
        temp_path.append(node)
    else:
        #Copy path till last_fork
        #Slice obsolete rest of num_of_childs_left
        temp_path = single_paths[-1][:last_fork+1]
        num_of_childs_left = num_of_childs_left[:last_fork+1]
        node = single_paths[-1][last_fork]

#adds one step to the path
#deal with key lookup error if there is a ref to a not existing node
    while len(paths['nodes'][node]) != 0:
        #Bug: Endnote will not be recorded or?
        try:
    #Check if node is not called the first time
            left = num_of_childs_left[len(temp_path)-1]
            num_childs = len(paths['nodes'][node])
            temp_path.append(paths['nodes'][node][num_childs-left])
            try:
                num_of_childs_left[len(temp_path)-1] -= 1
            except IndexError:
                num_of_childs_left[-1] -= 1
            node = paths['nodes'][node][num_childs-left]
    #If node is called the fist time
        except IndexError:
            #temp_path.append(node)
            temp_path.append(paths['nodes'][node][0])
            num_of_childs_left.append(len(paths['nodes'][node])-1)
            node = paths['nodes'][node][0]

    #If while loop ends, we reached an end node
    else:
        single_paths.append(temp_path)
        if all(i <= 0 for i in num_of_childs_left):
            return single_paths
        else:
            for i in range(len(num_of_childs_left)-1, 0, -1):
                if num_of_childs_left[i] > 0:
                    last_fork = i
                    break
            iterator(paths, num_of_childs_left, single_paths, last_fork)












# wenn node id in all, aber nicht in gecheckter liste/nicht aktiviert wurde -> nicht mit Start verknüpft
#     and end node, no repetition in path
# check if all answer have reference
