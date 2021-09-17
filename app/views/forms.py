from django import forms
from django.forms import ModelForm

from authentication.models import User, UserProfile, ROLE_TYPES


class UserFormWithoutPassword(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control only_add'}),
        }


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'office']
        widgets = {
            'role': forms.Select(attrs={'class': 'select2 select2-modal'}, choices=ROLE_TYPES),
            'office': forms.Select(attrs={'class': 'select2 select2-modal'})
        }
