

'''
    def product_create_view(request):
        form = ProductForm(request.POST or None)
        if form.is_valid():
            form.save()
            form = ProductForm()
        context = {
        'form' : form
        }
        return render(request, 'product/product_create.html', context)
'''



test = {
'id': '78324628936498234692346',
'name': 'Herkunftsland',
'question': 'Wo?',
'answer_type': 'select',
'answers': ['Arbeitserlaubnis', 'Gestattung', 'Duldung'],
'checks': None,
'condition': {
    'type': 'JSONlogic'
    "if":[{"<": [{"var":"input"}, 4] }, 0,
        {">": [{"var":"input"}, 4] }, 1],
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









sudo apt-get --purge remove pgdg-keyring postgresql-10 postgresql-client-10 postgresql-client-common
a
