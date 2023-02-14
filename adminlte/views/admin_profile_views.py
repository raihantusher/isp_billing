from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required

from store.models import ReviewRating
from store.forms import ReviewForm
from accounts.models import UserProfile, Account
from django.contrib.admin.views.decorators import staff_member_required


class ProfileList(ListView):
    model = UserProfile
    context_object_name = "profile_list"
    template_name = 'dashboard/pages/profile_list.html'
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return UserProfile.objects.filter(name__startswith=query)
        else:
            return UserProfile.objects.order_by("-id")

    #
    # def get_context_data(self, *args, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     data['page_title'] = 'Authors'
    #     return data

staff_member_required
def view_profile(request, id):
    profile = UserProfile.objects.get(pk=id)
    orders = profile.user.order_set.filter(status="Delivered").order_by('-id')

    total_order = profile.user.order_set.filter(status="Delivered").count()
    total_spent = 0

    for order in orders:
        total_spent += order.order_total


    context = {
        'profile': profile,
        'orders' : orders,
        'total_spent':total_spent,
        'total_order': total_order
    }
    return render(request, 'dashboard/pages/view_profile.html', context)
