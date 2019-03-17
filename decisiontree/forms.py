from django import forms
from .models import Product
from django.forms.formsets import BaseFormSet

class NodeForm(forms.Form):
    INPUT_CHOICES = (
    ('button', 'Buttons'),
    ('list', 'Auswahlliste'),
#    ('multiple_select', 'Mehrfachauswahl'),
#    ('short_text', 'Textfeld'),
#    ('long_text', 'Großes Textfeld'),
    ('number', 'Zahleneingabe'),
    ('date', 'Datum')
    )

    name = forms.CharField(label='Name für den Knoten')
    question = forms.CharField(label='Frage')
    example = forms.CharField(label='Möchtest du Beispiele geben?', required=False)
    image = forms.ImageField(required=False)
    input_type = forms.ChoiceField(label='Eingabeart', choices = INPUT_CHOICES)

class ButtonAnswersForm(forms.Form):
    answer = forms.CharField(label='Antwort')

class ListAnswersForms(forms.Form):
    answer = forms.CharField(widget=forms.Textarea, label='Liste aller Antwortmöglichkeiten')

#Disabled till integration of AND/OR
#class MultipleSelectAnswersForm(forms.Form):
    #answer = forms.CharField(label='Antwort')


#Num and Date Forms could be empty
class NumberAnswersForm(forms.Form):
    pass
#    rule = forms.CharField(label='Speichern als')

class DateAnswerForm(forms.Form):
    pass
#    rule = forms.CharField(label='Speichern als')


#Build seperate getInfo-Node, with possibility to set label, type of input, no. per field
#class ShortTextAnswersForm(forms.Form):
#    answer = forms.CharField(label='Antwort')
#    rule = forms.CharField(label='Speichern als')

#class LongTextAnswersForm(forms.Form):
#    answer = forms.CharField(widget=forms.Textarea, label='Antwort')
#    rule = forms.CharField(label='Speichern als')



class LogicForm(forms.Form):
    operators = forms.ChoiceField(label='Operator', choices = [])
    antworten = forms.ChoiceField(label='Mögliche Antworten', choices = [])
    action = forms.ChoiceField(label='Action', choices = (
    ('go_to', 'gehe zu'),
#    ('set', 'setze')
    ))
    var_to_modify = forms.CharField(label='Object to perform action on')

    def __init__(self, *args, **kwargs):
        self.test1 = kwargs.pop('test1', None)
        self.input_type = kwargs.pop('input_type', None)
        self.action = kwargs.pop('action', None)
        super(LogicForm, self).__init__(*args, **kwargs)

#        if self.action == 'go_to':
#            self.fields['var_to_modify'].widget = forms.ChoiceField()

#        elif self.action == 'set':
#            self.fields['var_to_modify'].widget = forms.CharField()
#            self.fields['value_to_set'] = forms.CharField()

        if self.input_type == 'button':
            self.fields['operators'].choices = (
            ('==', 'gleich'),
            ('!=', 'nicht'))

        elif self.input_type == 'list':
            self.fields['antworten'] = forms.CharField(widget=forms.Textarea)
            self.fields['operators'].choices = (
            ('==', 'gleich'),
            ('!=', 'nicht'))

#        elif self.input_type == 'multiple_select':
#            pass

#        elif self.input_type == 'short_text':
#            self.fields['to'] = forms.CharField()
#            pass

#        elif self.input_type == 'long_text':
#            self.fields['to'] = forms.CharField()
#            pass

        elif self.input_type == 'number':
            self.fields['antworten'] = forms.FloatField()
            self.fields['operators'].choices = (
            ('==', 'gleich'),
            ('!=', 'nicht'),
            ('<', 'kleiner als'),
            ('<=', 'kleiner gleich'),
            ('>', 'größer als'),
            ('>=', 'größer gleich')
            )

        elif self.input_type == 'date':
            self.fields['antworten'] = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
            self.fields['operators'].choices = (
            ('==', 'gleich'),
            ('!=', 'nicht'),
            ('<', 'kleiner als'),
            ('<=', 'kleiner gleich'),
            ('>', 'größer als'),
            ('>=', 'größer gleich')
            )
        else:
            pass
