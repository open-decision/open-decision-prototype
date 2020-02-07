import os
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
from datetime import date
from django.core import serializers
from django.http import JsonResponse
from django.utils.translation import gettext as _
from pages.models import PublishedTree

VERSION = 0.1
LOGIC_TYPE = 'jsonLogic version X'

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
def published_tree_view(request):
    if request.method == 'GET':
        context = {
         'published_tree_list': PublishedTree.objects.filter(owner=request.user),
         }
    return render(request, 'published_trees.html', context)

@login_required
def add_tree(request):
    f = DecisionTreeForm(request.POST)
    try:
        if f.is_valid():
            tree = f.save(commit=False)
            tree.owner = request.user
            tree.save()
    except IntegrityError as e:
        return HttpResponse('<div class="border-left-danger pl-2">'+ _('<p>Please choose another name, this one is  already taken.</p>') + '</div>')
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
def unpublish_tree (request):
    id = request.POST.get('tree_id')
    id_clean = bleach_clean(id)
    print(id_clean)
    PublishedTree.objects.filter(id=id_clean).delete()
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
    if os.environ.get('DJANGO_PRODUCTION') is not None:
        context = {
        'production' : 'true',
        'selected_tree' : DecisionTree.objects.get(slug=slug),
        }
        return render(request, 'export.html', context)
    else:
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
    # todo: are answers matching to logic? button -> make field not editable; how to check others?
    all = Node.objects.filter(decision_tree__slug=slug)
    end_nodes = all.filter(end_node=True)
    no_end_nodes = all.filter(end_node=False)

# Build errors dict for nodes without data_answer or data_logic
#todo: data answer und logic can contain [{}] as well
    errors = {
        'no_answers': [n.id for n in no_end_nodes.filter(data_answer='[]')],
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
            print('Called first time')
    # If node is called the first time
        except IndexError:
            temp_path.append(paths['nodes'][node]['childs'][0])
            paths['accessed_nodes'].append(paths['nodes'][node]['childs'][0])
            num_of_childs_left.append(len(paths['nodes'][node]['childs'])-1)
            node = paths['nodes'][node]['childs'][0]
            print('Called second time')
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

@login_required
def export_file (request, slug):
    export = build_tree(slug)
    response = JsonResponse(export, safe=False, content_type='application/json', json_dumps_params={'indent': 2})
    response['Content-Disposition'] = 'attachment; filename="{}.json"'.format(slug)
    return response


def build_tree (slug):
    # Build localization input
    # pass all_nodes
    all_nodes = Node.objects.filter(decision_tree__slug=slug)
    export = {}
# Set some header data to ensure proper processing of the created tree
    export['header'] = {
        'version' : VERSION,
        #'localization': request.POST.get('localization', 'de-de'),
        'build_date': date.today(),
        'logic_type': LOGIC_TYPE,
        'owner': DecisionTree.objects.get(slug=slug).owner.username,

        'tree_name' : DecisionTree.objects.get(slug=slug).name,
        'tree_slug' : slug,
        'start_node': all_nodes.get(start_node = True).slug,
        'vars': {},
    }

# Set the data that can be copied from the database
    for n in all_nodes:
        export[n.slug] = {
        'name': n.name,
        'question': n.question,
        'input_type': n.input_type,
        'end_node': n.end_node,
        'rules': {},
        }
# Build the answer value according to the selected input_type
# When the user needs to enter a number, date or if the node is an end-node, no
# answers need to be displayed
        if (n.input_type == 'number') or (n.input_type == 'date') or (n.input_type == 'end_node'):
            export[n.slug]['answers'] = []
        elif n.input_type == 'button':
            export[n.slug]['answers'] = [single_answer['answer'] for single_answer in json.loads(n.data_answer)]
# For lists answers separated by line breaks are split into a list of single answers
        elif n.input_type == 'list':
            export[n.slug]['answers'] = json.loads(n.data_answer)[0]['answer'].splitlines()

# Build the logic dict

#todo: refactor code to use a counter within the forloop to know if the dict exists
#todo: option to set a value for variables

        for l in json.loads(n.data_logic):
            # Loop through logic forms

            if (n.input_type == 'number') or (n.input_type =='date') or (n.input_type == 'button'):
                # Build the rules first
                # If dict already exists
                try:
                    export[n.slug]['rules']['if'].extend(
                    [
                        {l['operator']: [{"var":"answer"}, l['answers_logic']]},
                        str(int(len(export[n.slug]['rules']['if'])/2)),
                        ])
                # If dict does not exist
                except KeyError:
                    export[n.slug]['rules'] = {
                    'if' : [
                        {l['operator']: [{"var":"answer"}, l['answers_logic']]}, "0",
                    ]}

                # Then build the  results block
                if l['action'] == 'go_to':
                    data = {'destination': all_nodes.get(id = l['var_to_modify']).slug}

                # Commented out as the value for the var cannot be set yet
                # elif l['action'] == 'set'::
                #     data = {'set': {
                #         'name': l['var_to_modify'],
                #         'value': # cannot be set by user yet
                #         }}
                #
                #     export['header']['vars'][l['var_to_modify']] = {
                #     'type': '',
                #     'set_in_node': n.slug,
                #     }


            elif n.input_type == 'list':
                try:
                    export[n.slug]['rules']['if'].extend(
                    [
                        {'in': [{"var":"answer"}, l['answers_logic'].splitlines()]},
                        str(int(len(export[n.slug]['rules']['if'])/2)),
                        ])
                # If dict does not exist
                except KeyError:
                    export[n.slug]['rules'] = {
                    'if' : [
                        {'in': [{"var":"answer"}, l['answers_logic'].splitlines()]}, "0",
                    ]}

                # Then build the  results block
                if l['action'] == 'go_to':
                    data = {'destination': all_nodes.get(id = l['var_to_modify']).slug}

            try:
                export[n.slug]['results'][str(int(len(export[n.slug]['results'])))] = data
            except KeyError:
                export[n.slug]['results'] = {}
                export[n.slug]['results']['0'] = data
    return export

@login_required
def load_tree(request):
    selected_tree = request.GET.get('selected_tree')
    data = build_tree(selected_tree)
    return JsonResponse(data, safe=False)
