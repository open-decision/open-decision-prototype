import os, json
from django.shortcuts import render, redirect
from django.views import generic
from .models import DecisionTree, Node
from .forms import DecisionTreeForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.db.models import Count
from django.http import HttpResponse
from .models import bleach_clean
from django.db import IntegrityError
from datetime import date
from django.core import serializers
from django.http import JsonResponse
from django.utils.translation import gettext as _
from pages.models import PublishedTree
from users.models import CustomUser, Profile
from django.conf import settings

@login_required
def dashboard_view(request):
    if request.method == 'GET':
        form = DecisionTreeForm()
        context = {
         'decisiontree_list': DecisionTree.objects.filter(owner=request.user).annotate(node_number=Count("node")),
         'form':form,
         }
        if request.user.profile.saw_dashboard:
             context['start_tour'] = False
        else:
            context['start_tour'] = True
            user_profile = Profile.objects.get(user=request.user)
            user_profile.saw_dashboard = True
            user_profile.save(update_fields=['saw_dashboard'])
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
    except IntegrityError:
        return HttpResponse('<div class="border-left-danger pl-2">'+ _('<p>Please choose another name, you already have a tree with this name.</p>') + '</div>')
    context = {
     'decisiontree_list': DecisionTree.objects.filter(id=tree.id),
     'node_num': DecisionTree.objects.filter(owner=request.user).count(),
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
    existing_nodes = Node.objects.filter(decision_tree__owner=request.user).filter(decision_tree__slug=slug).filter(new_node=False).order_by('-created_at')
    new_nodes = Node.objects.filter(decision_tree__owner=request.user).filter(decision_tree__slug=slug).filter(new_node=True).order_by('-created_at')

    if request.method == 'GET':
        context = {
        'existing_nodes': existing_nodes,
         'new_nodes': new_nodes,
         'selected_tree': DecisionTree.objects.filter(owner=request.user).filter(slug=slug).values()[0]
         }
    return render(request, 'tree_view.html', context)

@login_required
def export_tree(request, slug):
    if True:#os.environ.get('DJANGO_PRODUCTION') is not None:
        context = {
        'production' : 'true',
        'selected_tree' : DecisionTree.objects.filter(owner=request.user).get(slug=slug),
        }
        return render(request, 'export.html', context)
    else:
        data = check_tree(slug, request)
        errors = data[0]
        all_nodes = data[1]
        errors['no_answers'] = [all_nodes.get(id=element) for element in errors['no_answers']]
        errors['no_logic'] = [all_nodes.get(id=element) for element in errors['no_logic']]
        errors['no_ref_to_start'] = [all_nodes.get(id=element) for element in errors['no_ref_to_start']]
        errors['no_var'] = {all_nodes.get(id=key):value for (key,value) in errors['no_var'].items()}
        errors['no_ref_to_end'] = [[all_nodes.get(id=node) for node in path] for path in errors['no_ref_to_end']]
        errors['not_end_nodes'] = list(set([path[-1] for path in errors['no_ref_to_end']]))
        errors['selected_tree'] = DecisionTree.objects.filter(owner=request.user).get(slug=slug)
        print(errors)
        return render(request, 'export.html', errors)


def check_tree(slug, request):
    # Build dic with tree structure to check tree integrity
    # todo: are answers matching to logic? button -> make field not editable; how to check others?
    all = Node.objects.filter(decision_tree__owner=request.user).filter(decision_tree__slug=slug)
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
                if d['target'] == '':
                    errors['no_var'][n.id] = d['answers_logic']
                else:
                    l.append(d['target'])
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
    Node.objects.filter(decision_tree__owner=request.user).filter(slug=slug).update(end_node= True)
    return HttpResponse()

@login_required
def delete_node (request):
    id = request.POST.get('node_id')
    Node.objects.filter(id=id).delete()
    return HttpResponse()

@login_required
def export_file (request, slug):
    export = build_tree(slug, request)
    response = JsonResponse(export, safe=False, content_type='application/json', json_dumps_params={'indent': 2})
    response['Content-Disposition'] = 'attachment; filename="{}.json"'.format(slug)
    return response


def build_tree (slug, request):
    # Build localization input
    # pass all_nodes
    all_nodes = Node.objects.filter(decision_tree__owner=request.user).filter(decision_tree__slug=slug)
    export = {}
# Set some header data to ensure proper processing of the created tree
    export['header'] = {
        'version' : settings.DATAFORMAT_VERSION,
        #'localization': request.POST.get('localization', 'de-de'),
        'build_date': date.today(),
        #'logic_type': settings.LOGIC_TYPE,
        #'owner': DecisionTree.objects.filter(owner=request.user).get(slug=slug).owner.username,

        'tree_name' : DecisionTree.objects.filter(owner=request.user).get(slug=slug).name,
        'tree_slug' : slug,
        'start_node': all_nodes.get(start_node = True).slug,
        'vars': {},
    }

# Set the data that can be copied from the database
    for n in all_nodes:
        export[n.slug] = {
        'name': n.name,
        'text': n.question,
        'inputs': [],
        'rules': {},
        'destination': {},
        'action': {},
        }

        try:
            input_type = json.loads(n.inputs)[0]['input_type']
        except (KeyError, IndexError):
            input_type = 'button'

        if input_type not in ['button','free_text', 'end_node']:
            data_input = json.loads(n.inputs)
            data_logic = data_input.pop()
        else:
            data_input = json.loads(n.inputs)
            data_logic = None

        for idx, i in enumerate(data_input):

# Build the answer value according to the selected input_type
# When the user needs to enter a number, date or if the node is an end-node, no
# answers need to be displayed

            if input_type == 'button':
            # Each button  is one input in the  builder atm but saved as one
            # input elem in the dataformat
                try:
                    #Check if a list of buttons already exist
                    if export[n.slug]['inputs'][-1]['type'] == 'buttons':
                        export[n.slug]['inputs'][-1]['options'].append(i['text'])
                    else:
                    #If the existing last input elem was not for buttons
                        export[n.slug]['inputs'].append(
                        {
                        'type': 'buttons',
                        'display_as': 'buttons',
                        'label': '',
                        'options': [i['text']]
                        })
                except IndexError:
                    #If no inputs exist yet
                    export[n.slug]['inputs'].append(
                    {
                    'type': 'buttons',
                    'display_as': 'buttons',
                    'label': '',
                    'options': [i['text']]
                    })
                # Add destination
                export[n.slug]['destination'][i['text']] = all_nodes.get(id = i['destination']).slug

            elif input_type == 'list':
                export[n.slug]['inputs'].append(
                {
                'type': 'list',
                'label': '',
                # For lists answers separated by line breaks are split into a list of single answers
                'options': [single_answer.strip() for single_answer in i['text'].splitlines()],
                })

            elif input_type == 'number':
                export[n.slug]['inputs'].append(
                {
                'type': 'number',
                'label': '',
                })

            elif input_type == 'free_text':
                if 'destination' in i:
                    export[n.slug]['destination']['default'] = all_nodes.get(id = i['destination']).slug

                export[n.slug]['inputs'].append(
                {
                'type': i['validation'],
                'label': i['text'],
                'id': slugify(i['text'])
                })

            # End-nodes have no inputs by  definition
            elif input_type == 'end_node':
                export[n.slug]['inputs'] = []
                break


# Build the logic dict

#todo: refactor code to use a counter within the forloop to know if the dict exists
#todo: option to set a value for variables
        if data_logic:
            for idx, l in enumerate(data_logic):
                # Loop through logic forms

                if (input_type == 'number') or (input_type =='date'):
                    # Build the rules first
                    # If dict already exists
                    if 'if' in export[n.slug]['rules']:
                        export[n.slug]['rules']['if'].extend(
                        [
                            {l['operator']: [{"var":"a"}, l['compare_to']]},
                            str(idx),
                            ])
                    # If dict does not exist
                    else:
                        export[n.slug]['rules'] = {
                        'if' : [
                            {l['operator']: [{"var":"a"}, l['compare_to']]}, "0",
                        ]}

                    # Then build the results block - the old way
                    #if l['action'] == 'go_to':
                    #data = {'destination': all_nodes.get(id = l['target']).slug}

                    export[n.slug]['destination'][str(idx)] = all_nodes.get(id = l['target']).slug

                    # Commented out as the value for the var cannot be set yet
                    # elif l['action'] == 'set'::
                    #     data = {'set': {
                    #         'name': l['target'],
                    #         'value': # cannot be set by user yet
                    #         }}
                    #
                    #     export['header']['vars'][l['target']] = {
                    #     'type': '',
                    #     'set_in_node': n.slug,
                    #     }

                elif input_type == 'list':

                    if 'if' in export[n.slug]['rules']:
                        compare_to_split = [single_answer.strip() for single_answer in l['compare_to'].splitlines()]
                        export[n.slug]['rules']['if'].extend(
                        [
                            {'in': [{"var":"a"},compare_to_split]},
                            str(idx),
                            ])

                    # If dict does not exist
                    else:
                        compare_to_split = [single_answer.strip() for single_answer in l['compare_to'].splitlines()]
                        export[n.slug]['rules'] = {
                        'if' : [
                            {'in': [{"var":"a"}, compare_to_split]}, "0",
                        ]}

                    # Then build the results block
                    #if l['action'] == 'go_to':
                    #data = {'destination': all_nodes.get(id = l['target']).slug}
                    export[n.slug]['destination'][str(idx)] = all_nodes.get(id = l['target']).slug

            #End of the loop for l in logic

    return export

@login_required
def load_tree(request):
    selected_tree = request.GET.get('selected_tree')
    data = build_tree(selected_tree, request)
    return JsonResponse(data, safe=False)
