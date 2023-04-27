from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols':60, 'rows':10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) >200:
            raise ValidationError('Слишком длинный заголовок, сократите пожалуйста')

        return title


class AddSpForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = '__all__'



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))


class ChoiceWidget(forms.ChoiceField.widget):
    def value_from_datadict(self, data, files, name):
        return data.get(name)

class ContactForm(forms.ModelForm):
    class Meta:
        model= Contact
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput(attrs={"class":"editContact"}),
            'role': ChoiceWidget(choices=[('sponsor', 'Спонсор'), ('organizer', 'Организатор')])
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['message'].required = False





