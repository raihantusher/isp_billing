from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
# from verify_email.email_handler import send_verification_email

from adminlte.forms import LoginForm, SignUpForm, SettingForm
from store.models import Setting
from accounts.models import UserProfile, Account
from django.shortcuts import get_object_or_404
from accounts.forms import UserForm, UserProfileForm
from django.contrib.admin.views.decorators import staff_member_required


def login(request):
    if request.user.is_authenticated:
        return redirect("seller_dashboard")
    else:
        form = LoginForm()
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                raw_password = form.cleaned_data['password']
                user = authenticate(email=email, password=raw_password)
                if user is not None:
                    auth_login(request, user)
                    # messages.success(request, "User is logged in succ")
                else:
                    messages.info(request, "Email or Password is incorrect.")
            return redirect("seller_login")
    return render(request, 'dashboard/login.html', {"form": form})


'''
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
'''

def logout_user(request):
    logout(request)
    return redirect("seller_login")

@staff_member_required
def store_settings(request, id):
    setting = Setting.objects.filter(id=id).last()
    setting_form = SettingForm(instance=setting)
    if request.method == "POST":
        setting_form = SettingForm(instance=setting, data=request.POST, files=request.FILES)
        setting_form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'setting_form': setting_form
    }
    return render(request, 'dashboard/pages/store_setting.html', context)

@staff_member_required
def profile_settings(request):
    userprofile = UserProfile.objects.filter(user=request.user).last()
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile_settings')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'dashboard/pages/edit_profile.html', context)


@login_required(login_url='login')
def password_settings(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('password_settings')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('password_settings')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('password_settings')
    return render(request, 'dashboard/pages/edit_password.html')
