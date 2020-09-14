from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

passwordInputWidget = {
    'password': forms.PasswordInput(),
}


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = [passwordInputWidget]


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = [passwordInputWidget]


class RegistrateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']
