from django import forms
from django.forms import ModelForm
from .models import DecisionTree
from django.utils.text import slugify

class DecisionTreeForm(ModelForm):
    class Meta:
        model = DecisionTree
        exclude = ('owner','slug')

    def save(self, *args, **kwargs):
        if self.instance.pk:
            return super(DecisionTreeForm, self).save()

        instance = super(DecisionTreeForm, self).save(commit=False)
        instance.slug = slugify(instance.name)
        instance.save()

        return instance
