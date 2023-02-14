from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView

from adminlte.forms import PaymentForm
from orders.models import Payment
from django.contrib.admin.views.decorators import staff_member_required


class PaymentList(ListView):
    model =  Payment
    context_object_name = "payment_list"
    template_name = 'dashboard/pages/payment_list.html'
    paginate_by = 25


    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Payment.objects.filter(
                Q(payment_id__icontains=query)
            )
        else:
            return Payment.objects.order_by("-id")

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = 'Authors'
        return data

@staff_member_required
def edit_payment(request, id ):
    payment = Payment.objects.get(pk=id)
    payment_form = PaymentForm(instance=payment)

    if request.method == "POST":
        payment_form = PaymentForm(instance=payment , data = request.POST)
        payment.save()
        messages.success(request, f' {payment.payment_id} is updated successfully!')
        return redirect('payment_list')
    context = {
        'payment_form':payment_form
    }
    return render(request, 'dashboard/pages/edit_payment.html', context)

@staff_member_required
def delete_payment(request, id ):
    if request.method == "POST":
        payment = Payment.objects.get(pk=id)
        payment.delete()
        messages.success(request, 'Payment is deleted successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))