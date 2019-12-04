from django import forms
from django.forms.formsets import BaseFormSet

# from django import models
# class User(models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=50)
#     first_name = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
        'password': forms.PasswordInput(),
    }
