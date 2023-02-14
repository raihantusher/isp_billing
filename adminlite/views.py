from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from verify_email.email_handler import send_verification_email

from .forms import LoginForm, SignUpForm


# Create your views here.
@login_required(login_url="login/")
def index(request):
    print(request.user.username)
    return render(request, 'dashboard/index.html')


def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                raw_password = form.cleaned_data['password']
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    auth_login(request, user)
                    # messages.success(request, "User is logged in succ")
                else:
                    messages.info(request, "Username or Password is incorrect.")
            return redirect("/")
    return render(request, 'dashboard/login.html', {"form": form})


def signup(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        form = SignUpForm()
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            print(form.errors)
            if form.is_valid():
                inactive_user = send_verification_email(request, form)
                username = form.cleaned_data['username']
                raw_password = form.cleaned_data['password1']
                user = authenticate(username=username, password=raw_password)
                if user is not None:
                    auth_login(request, user)
                return redirect("/")

    return render(request, 'dashboard/signup.html', {"form": form})


def logout_user(request):
    logout(request)
    return redirect("login")
