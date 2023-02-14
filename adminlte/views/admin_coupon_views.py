from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView
from django.contrib import messages
from coupon.forms import CouponForm
from coupon.models import Coupon
from django.contrib.admin.views.decorators import staff_member_required


class CouponList(ListView):
    model = Coupon
    context_object_name = "coupon_list"
    template_name = 'dashboard/pages/coupon_list.html'
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Coupon.objects.filter(name__startswith=query)
        else:
            return Coupon.objects.order_by("-id")
    #
    # def get_context_data(self, *args, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     data['page_title'] = 'Authors'
    #     return data

@staff_member_required
def add_new_coupon(request):
    coupon_form = CouponForm()

    if request.method == "POST":
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            coupon_form.save()

    context = {
        'coupon_form': coupon_form
    }
    return render(request, 'dashboard/pages/add_new_coupon.html', context)

@staff_member_required
def edit_coupon(request, id):
    coupon = Coupon.objects.get(pk=id)
    coupon_form = CouponForm(instance=coupon)

    if request.method == "POST":
        coupon_form = CouponForm(instance=coupon, data=request.POST)
        coupon_form.save()
        messages.success(request, f' {coupon.coupon_code} is updated successfully!')
        return redirect('coupon_list')
    context = {
        'coupon_form': coupon_form
    }
    return render(request, 'dashboard/pages/add_new_coupon.html', context)

@staff_member_required
def delete_coupon(request, id):
    if request.method == "POST":
        coupon = Coupon.objects.get(pk=id)
        coupon.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
