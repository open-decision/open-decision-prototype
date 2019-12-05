from django.shortcuts import render, redirect
from django.views import generic
from .models import DecisionTree, Node
from .forms import DecisionTreeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.db.models import Count
import json
from django.http import HttpResponse
from .models import bleach_clean
from django.db import IntegrityError

@login_required
def dashboard_view(request):
    if request.method == 'GET':
        form = DecisionTreeForm()
        context = {
         'decisiontree_list': DecisionTree.objects.filter(owner=request.user).annotate(node_number=Count("node")),
         'form':form,
         }
    return render(request, 'dashboard.html', context)

@login_required
def add_tree(request):
    f = DecisionTreeForm(request.POST)
    try:
        if f.is_valid():
            tree = f.save(commit=False)
            tree.owner = request.user
            tree.save()
    except IntegrityError as e:
        return HttpResponse('<div class="border-left-danger pl-2"><p>Bitte wähle einen anderen Namen, dieser ist bereits vergeben.</p></div>')
    context = {
     'decisiontree_list': DecisionTree.objects.filter(id=tree.id)
     }
    return render(request, 'dashboard_table_row.html', context)

@login_required
def delete_tree (request):
    id = request.POST.get('tree_id')
    id_clean = bleach_clean(id)
    DecisionTree.objects.filter(id=id_clean).delete()
    #todo: look for return value, maybe sth like 200?
    return HttpResponse()

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

@login_required
def export_tree(request, slug):
    #selected_tree object
#1. Build header
#2.
    data = check_tree(slug)
    errors = data[0]
    all_nodes = data[1]

    errors['no_answers'] = [all_nodes.get(id=element) for element in errors['no_answers']]
    errors['no_logic'] = [all_nodes.get(id=element) for element in errors['no_logic']]
    errors['no_ref_to_start'] = [all_nodes.get(id=element) for element in errors['no_ref_to_start']]
    errors['no_var'] = {all_nodes.get(id=key):value for (key,value) in errors['no_var'].items()}
    errors['no_ref_to_end'] = [[all_nodes.get(id=node) for node in path] for path in errors['no_ref_to_end']]
    errors['not_end_nodes'] = list(set([path[-1] for path in errors['no_ref_to_end']]))
    errors['selected_tree'] = DecisionTree.objects.get(slug=slug)
    print(errors)
    return render(request, 'export.html', errors)


def check_tree(slug):
    # Build dic with tree structure to check tree integrity
    # todo: are answers matching to logic? buttons -> make field not editable; how to check others?
    tree_name = slug
    all = Node.objects.filter(decision_tree__slug=slug)
    end_nodes = all.filter(end_node=True)
    no_end_nodes = all.filter(end_node=False)

# Build errors dict for nodes without data_answer or data_logic
#todo: data answer und logic kann auch [{}] enthalten
    errors = {
        'no_answers': [n.id for n in no_end_nodes.filter(data_answer='[]' )],
        'no_logic': [n.id for n in no_end_nodes.filter(data_logic='[]')],
        'no_var':{},
        'no_ref_to_start':[],
        'no_ref_to_end':[],
        }
    paths = {'node_list':[], 'accessed_nodes':[], 'no_ref_to_end':[], 'ref_to_end': [], 'start_node': all.get(start_node=True).id, 'end_nodes':[], 'nodes':{}}
    for n in all:
        paths['node_list'].append(n.id)
        paths['nodes'][n.id]={'childs':[]}
        l = []
        for d in json.loads(n.data_logic):
            if d['action'] == 'go_to':
                if d['var_to_modify'] == '':
                    errors['no_var'][n.id] = d['answers_logic']
                else:
                    l.append(d['var_to_modify'])
        paths['nodes'][n.id]['childs'] = l
    paths['end_nodes'] = [e.id for e in end_nodes]
    build_paths(paths)

    single_paths = single_paths_final
    paths = paths_after_iterator
    errors['no_ref_to_end'] = paths['no_ref_to_end']
    # Added set to second after difference
    errors['no_ref_to_start'] = list(set(paths['node_list']).difference(set(paths['accessed_nodes'])))

    print(single_paths)
    print(paths)

    return [errors, all]


def build_paths(paths):
    if paths['nodes'][paths['start_node']] is None:
        return #some Error saying start is not connected
    single_paths = iterator(paths, [], [], 0)
    print('Iteration finished, reached build path')

def iterator(paths, num_of_childs_left, single_paths, last_fork):
# Builds one full path and is then called again
    temp_path = []

# Only in the first run for this tree
    if len(single_paths) == 0:
        node = paths['start_node']
        paths['accessed_nodes'].append(paths['start_node'])
        temp_path.append(node)
    else:
        #Copy path from start node to last_fork
        #Slice obsolete rest of num_of_childs_left, +1 because slicing is exclusive of the end
        temp_path = single_paths[-1][:last_fork+1]
        num_of_childs_left = num_of_childs_left[:last_fork+1]
        node = single_paths[-1][last_fork]
    # adds one step to the path
    # Todo: deal with key lookup error if there is a ref to a not existing/deleted node
    while len(paths['nodes'][node]['childs']) != 0:
        try:
            #Check if node is not called the first time
            #Fails for start node
            left = num_of_childs_left[len(temp_path)-1]
            num_childs = len(paths['nodes'][node]['childs'])
            temp_path.append(paths['nodes'][node]['childs'][num_childs-left])
            paths['accessed_nodes'].append(paths['nodes'][node]['childs'][num_childs-left])
            try:
                num_of_childs_left[len(temp_path)-1] -= 1
            except IndexError:
                num_of_childs_left[-1] -= 1
            node = paths['nodes'][node]['childs'][num_childs-left]
    # If node is called the first time
        except IndexError:
            temp_path.append(paths['nodes'][node]['childs'][0])
            paths['accessed_nodes'].append(paths['nodes'][node]['childs'][0])
            num_of_childs_left.append(len(paths['nodes'][node]['childs'])-1)
            node = paths['nodes'][node]['childs'][0]

    #If while loop ends, we reached an end node
    else:
        single_paths.append(temp_path)
        # Check if the temp path ends with an end-node
        if temp_path[-1] not in paths['end_nodes']:
            for i in range(len(temp_path) - last_fork-1):
                print("Iterator loop marking valid:", -i, "ID:", temp_path[-i-1])
                paths['no_ref_to_end'].append(temp_path)

        # When there are no childs left we generated all paths
        if all(i <= 0 for i in num_of_childs_left):
            print('Iteration finished')
            # Todo: return value instead of using a global variable
            global single_paths_final
            global paths_after_iterator
            single_paths_final = single_paths
            paths_after_iterator = paths

        else:
            # Get the last node that has a child left and set this as last_fork
            for i in range(len(num_of_childs_left)-1, 0, -1):
                if num_of_childs_left[i] > 0:
                    last_fork = i
                    break
            print('After loop: Temp_path', temp_path, 'last_fork', last_fork)
            print('Num of childs left: ', num_of_childs_left)
            iterator(paths, num_of_childs_left, single_paths, last_fork)


@login_required
def set_as_endnode (request):
    slug = request.POST.get('node_slug')
    Node.objects.filter(slug=slug).update(end_node= True)
    return HttpResponse()

@login_required
def delete_node (request):
    id = request.POST.get('node_id')
    Node.objects.filter(id=id).delete()
    return HttpResponse()
