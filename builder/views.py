from django.shortcuts import render, redirect

# Create your views here.
# Wann i/node id als string bzw. int
def build_tree_view(request):
    if request.method == 'POST' and request.POST.get('reset'):
        request.session.flush()

    elif request.method == 'POST' and request.POST.get('demo'):
        response = redirect('/builder_demo/')
        return response
    elif request.method == 'POST':
        i = request.session.get('id', 1)
        try:
            request.session['demo']
        except:
            request.session['demo'] = {}

        request.session['demo'][i] = {}
        request.session['demo'][i]['question'] = request.POST['question']

        request.session['demo'][i]['answers'] = []
        request.session['demo'][i]['answers'].append(request.POST['answer1'])
        request.session['demo'][i]['answers'].append(request.POST['answer2'])
        if not request.POST['answer3'] == '':
            request.session['demo'][i]['answers'].append(request.POST['answer3'])
        else:
            print('No third answer-answers')
        print(request.session['demo'][i]['answers'])
        request.session['demo'][i]['rules'] = {}
        request.session['demo'][i]['rules'][request.session['demo'][i]['answers'][0]]= request.POST['rule1']
        request.session['demo'][i]['rules'][request.session['demo'][i]['answers'][1]]= request.POST['rule2']
        if not request.POST['rule3'] == '':
            request.session['demo'][i]['rules'][request.session['demo'][i]['answers'][2]]= request.POST['rule3']
        else:
            print('No third answer-rules')
        print(request.session['demo'])
        context = request.session['demo']
        request.session['id'] = i + 1
    else:
        print (request.POST)
    context = {}
    return render(request, 'build_tree.html', context)



def builder_demo(request):
    if request.method == 'GET':
        context = {
        'question': request.session['demo']['1']['question'],
        'answers': request.session['demo']['1']['answers']}
        request.session['last_node'] = '1'

    elif request.method == 'POST':
        if request.POST.get('restart'):
            context = {
            'question': request.session['demo']['1']['question'],
            'answers': request.session['demo']['1']['answers']}
            request.session['last_node'] = '1'

        elif request.POST.get('back_to_builder'):
            last_node = request.session.get('last_node', '1')
            response = redirect('/builder/')
            context = {
            'question': request.session['demo']['1']['question'],
            'answers': request.session['demo']['1']['answers']}
            return response
        else:
            last_node = request.session.get('last_node', '1')
            #request.session.get('last_node', 1)
            context = {}
            answer_given = request.POST.get('action')
            print(answer_given)
            #try:
            next_node = request.session['demo'][last_node]['rules'][answer_given]
            #except:
                #for key in request.session['demo'][request.session['last_node']]['rules']:
                #    if key.startswith(answer_given):
                #        next_node = request.session['demo'][request.session['last_node']]['rules'][key]
            try:
                print(request.session['demo'][next_node]['question'])
                context['question'] = request.session['demo'][next_node]['question']
            except:
                context['question'] = 'Soweit ist dein Baum leider noch nicht gebaut.'
            context['answers'] = request.session['demo'][next_node]['answers']
            request.session['last_node'] = next_node
    return render(request, 'builder_demo.html', context)
