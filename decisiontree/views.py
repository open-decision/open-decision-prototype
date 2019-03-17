from django.shortcuts import render, redirect
from .forms import *
from django.forms import formset_factory

def product_create_view(request):
    if request.method == 'GET':
        node_form = NodeForm
        NodeButtonFormSet = formset_factory(ButtonAnswersForm)
        context = {
        'form': node_form,
        }
        return render(request, 'product/product_create.html', context)
    elif request.method == 'POST' and request.POST.get('save'):
        print (request.POST)
        clean_data(request)
        node_form = NodeForm
        context = {
        'form': node_form
        }
        return render(request, 'product/product_create.html', context)


def load_answer_field(request):
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
    return render(request, 'product/answer_field.html', context)

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
        pass
    return [answer_form, expandable]

def load_logic_field(request):
    input_type = request.GET['input_type']
    LogicFormSet = formset_factory(LogicForm)
    test1 = (
    ('button', 'Buttons'),
    ('list', 'Auswahlliste'),
    ('multiple_select', 'Mehrfachauswahl'),
    ('short_text', 'Textfeld'),
    ('long_text', 'Großes Textfeld'),
    ('number', 'Nummernfeld'),
    ('date', 'Datum')
    )
    if input_type == 'button':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'input_type': input_type}, prefix='logic')
    elif input_type == 'list':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'input_type': input_type}, prefix='logic')
    elif input_type == 'multiple_select':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'action': '', 'input_type': input_type}, prefix='logic')
    elif input_type == 'short_text':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'action': '', 'input_type': input_type}, prefix='logic')
    elif input_type == 'long_text':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'action': '', 'input_type': input_type}, prefix='logic')
    elif input_type == 'number':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'action': '', 'input_type': input_type}, prefix='logic')
    elif input_type == 'date':
        logic_form = LogicFormSet(form_kwargs={'test1': test1, 'action': '', 'input_type': input_type}, prefix='logic')
    else:
        raise Exception('Invalid input type.')
    context = {
    'logic': logic_form
    }
    return render(request, 'product/logic_field.html', context)



def clean_data(request):
    try:
        data_node = {
            'name'      : request.POST.get('name'),
            'question'  : request.POST.get('question'),
            'example'   : request.POST.get('example'),
            'image'     : request.POST.get('image'),
            'input_type': request.POST.get('input_type'),
            }
    except ValueError:
        raise ValueError('')
    try:
        data_answer_formset = {
            'answer-TOTAL_FORMS'  : int(request.POST.get('answer-TOTAL_FORMS')),
            'answer-INITIAL_FORMS': int(request.POST.get('answer-INITIAL_FORMS')),
            'answer-MIN_NUM_FORMS': int(request.POST.get('answer-MIN_NUM_FORMS')),
            'answer-MAX_NUM_FORMS': int(request.POST.get('answer-MAX_NUM_FORMS'))
        }
        # Raise error, if formset management form was modified so that data cannot be parsed to int()
    except ValueError:
        raise ValueError('Formset content has been tampered with')
    except TypeError:
        #Fine if no answers are given, throws TypeError during int()
        #Build handler to notify user
        pass
    data_answer = {}
    for i in range(data_answer_formset['answer-TOTAL_FORMS']):
        key = 'answer-{}-answer'.format(i)
        data_answer[key] = request.POST.get(key)
    node_form = NodeForm(data_node)
#Process errors properly -  build error dict, display to user
    if node_form.is_valid():
        node_cleaned = node_form.cleaned_data
        AnswerFormUsed = set_answer_form(node_form.cleaned_data['input_type'])[0]
        print(AnswerFormUsed)
        #Security issues:
        # - MIN and MAX forms are taken from user input -> hardcode allowances?
        # - data is not really cleaned, is int() enough?, escaping necessary?
        if (data_answer_formset['answer-MIN_NUM_FORMS'] <= data_answer_formset['answer-TOTAL_FORMS'] <= data_answer_formset['answer-MAX_NUM_FORMS']):
            answers_cleaned = {}
            if node_form.cleaned_data['input_type'] == 'list':
                try:
                    answer_form_instance = AnswerFormUsed({'answer': data_answer['answer-0-answer']})
                    answer_form_instance.is_valid()
                    answers_cleaned[0] = answer_form_instance.cleaned_data['answer']
                    answers_cleaned[0] = answers_cleaned[0].splitlines()
                    print(answers_cleaned[0])
                except:
                    raise ValueError('Invalid answers')
            else:
                for i in range(data_answer_formset['answer-TOTAL_FORMS']):
                    key = 'answer-{}-answer'.format(i)
                    try:
                        answer_form_instance = AnswerFormUsed({'answer': data_answer[key]})
                        answer_form_instance.is_valid()
                        answers_cleaned[i] = answer_form_instance.cleaned_data
                    except:
                            raise ValueError('Invalid answers')

    else:
        print(NodeForm.errors)
#    save_node(node_cleaned, data_answer_formset, answers_cleaned)

def save_node(node_cleaned, data_answer_formset, answers_cleaned):
    node = {}
    if node_cleaned['input_type'] == 'list':

        node['answers'][value]


    for key,value in node_cleaned:
        node[key] = value
    return
    pass


#button, list, number, date




'''
def product_create_view(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProductForm()
    context = {
    'form' : form
    }
    return render(request, 'product/product_create.html', context)'''
