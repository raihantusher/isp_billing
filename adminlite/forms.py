from django import forms
from django.forms import TextInput, PasswordInput, EmailInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"User Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Retype Password"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
