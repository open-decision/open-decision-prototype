from django import forms
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
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Knotenname', 'class' : 'node_create_name'}), max_length="15")
    question = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Frage'}), max_length="80")
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
    answers_logic = forms.CharField(label='wenn', required=False)
    operator = forms.ChoiceField(label='', choices = [], required=False)
    action = forms.ChoiceField(label='dann', required=False, choices = (
    ('go_to', 'gehe zu'),
#    ('set', 'setze')
    ))
    var_to_modify = forms.CharField(label='', required=False)

    def __init__(self, *args, **kwargs):
        self.input_type = kwargs.pop('input_type', None)
        self.action = kwargs.pop('action', None)
        super(LogicForm, self).__init__(*args, **kwargs)

#        if self.action == 'go_to':
#            self.fields['var_to_modify'].widget = forms.ChoiceField()

#        elif self.action == 'set':
#            self.fields['var_to_modify'].widget = forms.CharField()
#            self.fields['value_to_set'] = forms.CharField()

        if self.input_type == 'button':
            self.fields['operator'].choices = (
            ('==', 'vorliegt'),
            ('!=', 'nicht vorliegt'))

        elif self.input_type == 'list':
            self.fields['answers_logic'] = forms.CharField(widget=forms.Textarea, label='wenn')
            self.fields['operator'].choices = (
            ('==', 'vorliegt'),
            ('!=', 'nicht vorliegt'))

#        elif self.input_type == 'multiple_select':
#            pass

#        elif self.input_type == 'short_text':
#            self.fields['to'] = forms.CharField()
#            pass

#        elif self.input_type == 'long_text':
#            self.fields['to'] = forms.CharField()
#            pass

        elif self.input_type == 'number':
            self.fields['answers_logic'] = forms.FloatField()
            self.fields['operator'].choices = (
            ('==', 'gleich'),
            ('!=', 'nicht'),
            ('<', 'kleiner als'),
            ('<=', 'kleiner gleich'),
            ('>', 'größer als'),
            ('>=', 'größer gleich')
            )

        elif self.input_type == 'date':
            self.fields['answers_logic'] = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
            self.fields['operator'].choices = (
            ('==', 'gleich'),
            ('!=', 'nicht'),
            ('<', 'kleiner als'),
            ('<=', 'kleiner gleich'),
            ('>', 'größer als'),
            ('>=', 'größer gleich')
            )
        else:
            pass
