from django import forms
from django.forms.formsets import BaseFormSet
from ckeditor.widgets import CKEditorWidget
from django.utils.translation import gettext_lazy as _


class NodeForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Node name'), 'class' : 'node_create_name'}), max_length="25")
    question = forms.CharField(required=False, widget=CKEditorWidget())

class NodeFormVisualBuilder(NodeForm):
    question = forms.CharField(widget=CKEditorWidget(config_name='visualbuilder'))

class InputForm (forms.Form):
    INPUT_CHOICES = (
        ('button', _('Button')),
        ('list', _('Selectlist')),
    #    ('multiple_select', 'Mehrfachauswahl'),
        ('short_text', _('Short free text')),
    #    ('long_text', 'Großes Textfeld'),
        ('number', _('Numberfield')),
    #    ('date', _('Datefield')),
        ('end_node', _('End-node - no input')))
    input_type = forms.ChoiceField(choices = INPUT_CHOICES, label= _('Input Type'))
    text = forms.CharField()
    def __init__(self, *args, **kwargs):
        self.input_type = kwargs.pop('input_type', 'button')
        super(InputForm, self).__init__(*args, **kwargs)

        if self.input_type == 'button':
            self.fields['text'].widget.attrs['placeholder'] = _('Button Text')
            self.fields['destination'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Destination')}))

        if self.input_type == 'list':
            self.fields['text'] = forms.CharField(widget=forms.Textarea(attrs={'placeholder': _('List of all choices')}))

        if (self.input_type == 'number') or (self.input_type == 'date') or (self.input_type == 'end_node'):
            self.fields['text'].widget = forms.HiddenInput()

        if self.input_type == 'short_text':
            self.fields['text'].widget.attrs['placeholder'] = _('Label')
            #Deactivated until we send data from interpreter to someone
            # self.fields['required'] = forms.BooleanField()
            # self.fields['validation'] = forms.ChoiceField(label=_('then'), required=False, choices = (
            # ('mail', _('E-Mail')),
            # ('phone', _('Phone Number'))
            # )
            # )


class LogicForm(forms.Form):
    compare_to = forms.CharField()
    operator = forms.ChoiceField(label=_('If the  answer'), choices = [], required=False)
    target = forms.CharField(required=False, max_length="25")
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
            self.fields['compare_to'].widget = forms.Textarea()
            self.fields['operator'].choices = (
            ('==', _('is  in')),
            ('!=', _('is not in'))
            )

        elif self.input_type == 'short_text':
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
            self.fields['compare_to'] = forms.FloatField()
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
            self.fields['compare_to'] = forms.DateField(widget=forms.TextInput(attrs=
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

        # elif self.input_type == 'end_node':
        #     self.fields['operator'].choices = forms.HiddenInput()
        #     self.fields['answers_logic'] = forms.HiddenInput()
        #     self.fields['action'].choices = forms.HiddenInput()
        #     self.fields['target'].choices = forms.HiddenInput()
        else:
            pass


# class LogicForm(forms.Form):
#     operator = forms.ChoiceField(label=_('If the answer'), choices = [], required=False)
#     answers_logic = forms.CharField(label=_(''), required=False)
#     action = forms.ChoiceField(label=_('then'), required=False, choices = (
#     ('go_to', _('go to')),
#     ('set', _('set')))
#     )
#     target = forms.CharField(label='', required=False, max_length="25")
#
#     def __init__(self, *args, **kwargs):
#         self.input_type = kwargs.pop('input_type', None)
#         self.action = kwargs.pop('action', None)
#         super(LogicForm, self).__init__(*args, **kwargs)
#
# #        if self.action == 'go_to':
# #            self.fields['target'].widget = forms.ChoiceField()
#
# #        elif self.action == 'set':
# #            self.fields['target'].widget = forms.CharField()
# #            self.fields['value_to_set'] = forms.CharField()
#
#         if self.input_type == 'button':
#             self.fields['operator'].choices = (
#             ('==', 'vorliegt'),
#             ('!=', 'nicht vorliegt'))
#
#         elif self.input_type == 'list':
#             self.fields['answers_logic'] = forms.CharField(widget=forms.Textarea, label='wenn')
#             self.fields['operator'].choices = (
#             ('==', 'vorliegt'),
#             ('!=', 'nicht vorliegt'))
#
#         elif self.input_type == 'short_text':
#             self.fields['operator'] = forms.CharField(widget=forms.HiddenInput())
#             self.fields['answers_logic'] = forms.CharField(label='Nehme die Antwort aus')
#             self.fields['action'].choices = (
#             ('set', 'speicher den Wert als Variable'),
#             ('set', 'speicher den Wert als Variable'))
#             self.fields['action'].label = 'und dann'
#             self.fields['operator'].choices = (
#             ('==', 'gleich'),
#             ('==', 'gleich'))
#
#         elif self.input_type == 'long_text':
#             self.fields['operator'] = forms.CharField(widget=forms.HiddenInput())
#             self.fields['answers_logic'] = forms.CharField(label='Nehme die Antwort aus')
#             self.fields['action'].choices = (
#             ('set', 'speicher den Wert als Variable'),
#             ('set', 'speicher den Wert als Variable'))
#             self.fields['action'].label = 'und dann'
#             self.fields['operator'].choices = (
#             ('==', 'gleich'),
#             ('==', 'gleich'))
#
#         elif self.input_type == 'number':
#             self.fields['answers_logic'] = forms.FloatField()
#             self.fields['operator'].choices = (
#             ('==', 'gleich'),
#             ('!=', 'nicht'),
#             ('<', 'kleiner als'),
#             ('<=', 'kleiner gleich'),
#             ('>', 'größer als'),
#             ('>=', 'größer gleich')
#             )
#
#         elif self.input_type == 'date':
#             self.fields['answers_logic'] = forms.DateField(widget=forms.TextInput(attrs=
#                                 {
#                                     'class':'datepicker'
#                                 }))
#             self.fields['operator'].choices = (
#             ('==', 'gleich'),
#             ('!=', 'nicht'),
#             ('<', 'kleiner als'),
#             ('<=', 'kleiner gleich'),
#             ('>', 'größer als'),
#             ('>=', 'größer gleich')
#             )
#
#         # elif self.input_type == 'end_node':
#         #     self.fields['operator'].choices = forms.HiddenInput()
#         #     self.fields['answers_logic'] = forms.HiddenInput()
#         #     self.fields['action'].choices = forms.HiddenInput()
#         #     self.fields['target'].choices = forms.HiddenInput()
#         else:
#             pass
