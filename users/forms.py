from django.contrib.auth.forms import UserChangeForm
from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser


class CustomUserCreationForm(SignupForm):
    class Meta(SignupForm):
        model = CustomUser
        fields = ('first_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(max_length=30)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('first_name','email',)
