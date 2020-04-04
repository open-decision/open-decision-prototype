from django import forms
from django.forms.formsets import BaseFormSet
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext_lazy as _

INPUT_CHOICES = (
        ('button', _('Button')),
        ('list', _('Selectlist')),
    #    ('multiple_select', 'Mehrfachauswahl'),
        ('free_text', _('Free text')),
    #    ('long_text', 'Großes Textfeld'),
        ('number', _('Numberfield')),
    #    ('date', _('Datefield')),
        ('end_node', _('End-node - no input')))

VALIDATION_CHOICES = (
        ('short_text', _('Short Text')),
        ('long_text', _('Long Text')),
        ('number', _('Number')),
        #('e-mail', _('E-Mail')),
        #('phone', _('Phone Number')),
        )

class NodeForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Node name'), 'class' : 'node_create_name'}), max_length="25")
    question = forms.CharField(required=False, widget=CKEditorWidget())

class NodeFormVisualBuilder(NodeForm):
    question = forms.CharField(widget=CKEditorWidget(config_name='visualbuilder'))

class InputForm (forms.Form):
    input_type = forms.ChoiceField(required=False, choices = INPUT_CHOICES, label= _('Input Type'))
    text = forms.CharField(required=False)
    def __init__(self, *args, **kwargs):
        self.input_type = kwargs.pop('input_type', 'button')
        super(InputForm, self).__init__(*args, **kwargs)

        if self.input_type == 'button':
            self.fields['text'].widget.attrs['placeholder'] = _('Button Text')
            self.fields['destination'] = forms.CharField(required=False, max_length="25", widget=forms.TextInput(attrs={'placeholder': _('Destination')}))

        if self.input_type == 'list':
            self.fields['input_type'].default = INPUT_CHOICES[1][1]
            self.fields['text'] = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': _('List of all choices')}))

        if (self.input_type == 'number') or (self.input_type == 'date'):
            self.fields['text'].widget = forms.HiddenInput()

        if self.input_type == 'free_text':
            self.fields['text'].widget.attrs['placeholder'] = _('Label')
            #Deactivated until we send data from interpreter to someone
            # self.fields['required'] = forms.BooleanField()
            self.fields['validation'] = forms.ChoiceField(label=_('then'), required=False, choices = VALIDATION_CHOICES)

        if self.input_type == 'end_node':
            self.fields['input_type'].default = INPUT_CHOICES[4][1]
            self.fields['text'].widget = forms.HiddenInput()

class LogicForm(forms.Form):
    operator = forms.ChoiceField(label=_('If the  answer'), choices = [], required=False)
    compare_to = forms.CharField(required=False)
    target = forms.CharField(required=False, max_length="25", widget=forms.TextInput(attrs={'placeholder': _('Destination')}))
    action = forms.ChoiceField(label=_('then'), required=False, choices = (
    ('go_to', _('go to')),
    ('set', _('set'))
    )
    )


    def __init__(self, *args, **kwargs):
        self.input_type = kwargs.pop('input_type', 'button')
        self.action = kwargs.pop('action', 'go_to')
        super(LogicForm, self).__init__(*args, **kwargs)

#        if self.action == 'go_to':
#            self.fields['target'].widget = forms.ChoiceField()

#        elif self.action == 'set':
#            self.fields['target'].widget = forms.CharField()
#            self.fields['value_to_set'] = forms.CharField()

        if self.input_type == 'button':
            # self.fields['operator'].choices = (
            # ('==', _('is')),
            # ('!=', _('is not'))
            # )
            self.fields['compare_to'].widget=forms.HiddenInput()
            self.fields['operator'].widget = forms.HiddenInput()
            self.fields['action'].widget = forms.HiddenInput()
            self.fields['target'].widget = forms.HiddenInput()

        elif self.input_type == 'list':
            self.fields['action'].widget = forms.HiddenInput()
            self.fields['compare_to'].widget = forms.Textarea(attrs={'placeholder': _('Choices')})
            self.fields['operator'].widget = forms.HiddenInput()
#             self.fields['operator'].choices = (
#             ('==', _('is  in')),
# #            ('!=', _('is not in'))
#             )

        elif self.input_type == 'free_text':
            self.fields['compare_to'].widget=forms.HiddenInput()
            self.fields['operator'].widget = forms.HiddenInput()
            self.fields['action'].widget = forms.HiddenInput()
            self.fields['target'].widget = forms.HiddenInput()

        # elif self.input_type == 'long_text':
        #     self.fields['operator'] = forms.CharField(widget=forms.HiddenInput())
        #     self.fields['answers_logic'] = forms.CharField(label=_('Take the  answer from'))
        #     self.fields['action'].choices = (
        #     ('set', _('save value as')),
        #     ('set', _('save value as'))
        #     )
        #     self.fields['action']widget.attrs['placeholder'] = _('and then')
        #     self.fields['operator'].choices = (
        #     ('==', _('equal')),
        #     ('==', _('equal'))
        #     )

        elif self.input_type == 'number':
            self.fields['action'].widget = forms.HiddenInput()
            self.fields['compare_to'] = forms.FloatField(required=False)
            self.fields['operator'].choices = (
            ('==', _('equal')),
            ('!=', _('not')),
            ('<', _('less than')),
            ('<=', _('less than or equal')),
            ('>', _('greater')),
            ('>=', _('greater or equal'))
            )

        elif self.input_type == 'date':
            self.fields['action'].widget = forms.HiddenInput()
            self.fields['compare_to'] = forms.DateField(required=False, widget=forms.TextInput(attrs=
                                {
                                    'class':'datepicker'
                                }))
            self.fields['operator'].choices = (
        ('==', _('equal')),
        ('!=', _('not')),
        ('<', _('less than')),
        ('<=', _('less than or equal')),
        ('>', _('greater')),
        ('>=', _('greater or equal'))
        )

        elif self.input_type == 'end_node':
            self.fields['compare_to'].widget=forms.HiddenInput()
            self.fields['operator'].widget = forms.HiddenInput()
            self.fields['action'].widget = forms.HiddenInput()
            self.fields['target'].widget = forms.HiddenInput()
        else:
            pass
