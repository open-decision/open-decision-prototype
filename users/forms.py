from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('first_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control form-control-user', 'placeholder' : 'First Name'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control form-control-user', 'placeholder' : 'E-Mail'})
        self.fields['password1'].widget.attrs.update({'class' : 'form-control form-control-user', 'placeholder' : 'Password'})
        self.fields['password2'].widget.attrs.update({'class' : 'form-control form-control-user', 'placeholder' : 'Repeat Password'})

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('first_name','email',)
