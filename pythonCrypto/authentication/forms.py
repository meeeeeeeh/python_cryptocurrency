from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages


def forbidden_users(value):
    f_users = ['admin', 'login', 'logout', 'administrator', 'user',
               'root', 'email', 'delete']
    if value.lower() in f_users:
        raise ValidationError('Invalid name for user, this is reserved word.')


def invalid_user(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('this is an invalid user, do not use these chars: @, +, -')


def unique_user(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('user ith username already exists.')


def unique_emai(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('user ith this email already exists.')


class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input',
               'placeholder': 'Введите имя пользователя'}
    ), max_length=25, required=True)
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'input',
               'placeholder': 'Введите почту'}
    ), max_length=60, required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input',
               'placeholder': '******'}
    ), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input',
               'placeholder': '******'}
    ), required=True)

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'password')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(forbidden_users)
        self.fields['username'].validators.append(invalid_user)
        self.fields['username'].validators.append(unique_user)
        self.fields['email'].validators.append(unique_emai)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.errors['password'] = self.error_class(['Password do not match. Try again'])
        return self.cleaned_data


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input',
               'placeholder': 'Введите имя пользователя'}
    ), max_length=25, required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input',
               'placeholder': '******'}
    ), required=True)

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Неверный логин или пароль")

    class Meta:
        model = User
        fields = ('username',
                  'password')