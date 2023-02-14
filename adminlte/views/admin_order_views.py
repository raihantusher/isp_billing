import json
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView

from django.template.loader import render_to_string
from django.core.mail import  EmailMessage
from django.db.models import Q, Sum
from orders.models import Order
from store.models import Product
from ..utils.charts import months, colorPrimary, get_year_dict
from django.contrib.admin.views.decorators import staff_member_required



@staff_member_required(login_url="seller_login")
def index(request):
    today = date.today()
    order_today = Order.objects.filter(created_at__day=today.day)
    best_selling_products = Product.objects.annotate(quantity_sum=Sum("orderproduct__quantity")).order_by(
        "-quantity_sum")[:15]
    sorted_by_views = Product.objects.all().order_by('-views')[:15]

    #
    # grouped_purchases = Order.objects.annotate(year=ExtractYear('created_at')).values('year').order_by('-year').distinct()
    # options = [purchase['year'] for purchase in grouped_purchases]
    # print(grouped_purchases)
    # print(options)
    context = {
        'best_selling_products': best_selling_products,
        'sorted_by_views': sorted_by_views,
        'order_today': order_today
    }
    return render(request, 'dashboard/pages/home.html', context)

@staff_member_required
def get_sales_chart(request, year):
    purchases = Order.objects.filter(created_at__year=year, status="Delivered")
    grouped_purchases = purchases.annotate(month=ExtractMonth('created_at')) \
        .values('month').annotate(average=Sum('order_total')).values('month', 'average').order_by('month')

    sales_dict = get_year_dict()

    for group in grouped_purchases:
        sales_dict[months[group['month'] - 1]] = round(group['average'], 2)

    return JsonResponse({
        'title': f'Sales in {year}',
        'data': {
            'labels': list(sales_dict.keys()),
            'datasets': [{
                'label': 'Amount ($)',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': list(sales_dict.values()),
            }]
        },
    })


class OrderList(ListView):
    model = Order
    context_object_name = "order_list"
    template_name = 'dashboard/pages/order_list.html'
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get("search")

        if query:
            return Order.objects.filter(
                Q(order_number__icontains=query)
            )
        else:
            return Order.objects.order_by("-id")

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = 'Authors'
        return data

@staff_member_required
def order_detail(request, id):
    order = Order.objects.get(pk=id)
    order_products = order.order_products.all()

    payments = order.payments.aggregate(paid=Sum("amount_paid"))
    paid = payments['paid']
    if paid  is None:
        paid = 0
    #print(payments)
    #
    # order_products = OrderProduct.objects.get(order=order) \
    #     .select_related('product') \
    #     .select_related('user') \
    #     .select_related('order')

    context = {
        'order': order,
        'order_products': order_products,
        'paid' : paid,
        'payable': order.order_total
    }
    return render(request, 'dashboard/pages/order_detail.html', context)

@staff_member_required
def delete_order(request, id):
    if request.method == "POST":
        order = Order.objects.get(pk=id)
        order.delete()
        messages.success(request, 'Order is deleted successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@staff_member_required
def change_in_order(request):
    context = {}

    if request.method == "POST":
        data = json.loads(request.body)
        order = Order.objects.get(pk=data['order_id'])

        if data["type"] == "shipping_charge_change":
            order.shipping_cost = data['shipping_cost']
            order.save()
            context['details'] = f"Shipping cost is now  updated"

        elif data["type"] == "order_status_change":
            order.status = data['status']
            order.save()

            mail_subject = f'Your order { order.order_number } is updated'
            message = render_to_string('mails/order_status_change.html', {
                'user': order.user,
                'order': order
            })
            to_email = order.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            context['details'] = f"Order status is now {order.status}"


    return JsonResponse(context)



