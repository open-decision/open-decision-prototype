@login_required
def node_edit_view(request, slug, node_slug):
    data_node = Node.objects.get(slug=node_slug)
    input_type = data_node.input_type
    node_form = NodeForm({'name': data_node.name, 'question': data_node.question, 'input_type': data_node.input_type})
    answer_form = load_answer_field(request, input_type, data_node)
    print(answer_form)
    context = {
        'form': node_form,
        'selected_tree': DecisionTree.objects.filter(slug=slug).values()[0],
        'answer_formset': answer_form[0],
        'expandable': answer_form[1],
        'logic_form': ''
        }
    return render(request, 'node_create.html', context)

  {% if answer_formset %}{% include "answer_field.html" %}{% endif %}

def load_answer_field(request, *args):
    try:
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
        return [answer_formset, expandable]



test = {
'id': '78324628936498234692346',
'name': 'Herkunftsland',
'question': 'Wo?',
'answer_type': 'select',
'answers': ['Arbeitserlaubnis', 'Gestattung', 'Duldung'],
'checks': None,
'condition': {
    'type': 'JSONlogic'
    "if":[{"<": [{"var":"input"}, 4] }, 0, {">": [{"var":"input"}, 4] }, 1],
        },
'result': {
    0 : {
        'destination': 'next Knoten',
        },
    1: {
        'destination': 'this Knoten',
        'set': {
            'name': 'höhe',
            'value': '3'
            }
        }
}

let i;
for (i = 0; i < 2; i++) {
console.log(test.rules[i]);
};




    json_data['name'] = node['name']
    json_data['question'] = node['question']
    json_data['input_type'] = node['input_type']
    json_data['checks'] = node['']





sudo apt-get --purge remove pgdg-keyring postgresql-10 postgresql-client-10 postgresql-client-common
a
