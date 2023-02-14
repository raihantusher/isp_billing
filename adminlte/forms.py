from django import forms
from django.forms import TextInput, PasswordInput, EmailInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from store.models import Product
from category.models import Category
from orders.models import Payment
from store.models import Article
from store.models import Setting

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"User Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Retype Password"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['created_date', 'modified_date']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category

        exclude = ('description',)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ('user', 'order',)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'