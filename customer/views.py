from django.shortcuts import render
from django.views.generic import ListView
#local
from customer.models import Customer
# Create your views here.


class CustomerList(ListView):
    model =  Customer
    context_object_name = "customer_list"
    template_name = 'panel/customer/list.html'

    def get_queryset(self):
        query = self.request.GET.get("s")
        if query:
            return Customer.objects.filter(name__startswith=query)
        else:
            return Customer.objects.order_by("-id")

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = 'Customers'
        return data