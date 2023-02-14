from django import template

from accounts.models import Account
from django.db.models import  Sum


from orders.models import Order, Product

register = template.Library()


@register.inclusion_tag('adminlte/comp/info_card.html')
def pending_order(**kwargs):
    try:
        order_count = Order.objects.filter(status="Pending").count()
    except Exception:
        order_count = 0

    return {
        'info': order_count,
        'info_bg': 'bg-danger',
        'info_icon': 'far fa-clock',
        'info_text': 'Pending Orders'
    }


@register.inclusion_tag('adminlte/comp/info_card.html')
def total_products(**kwargs):
    try:
        product_count = Product.objects.all().count()
    except Exception:
        product_count = 0

    return {
        'info': product_count,
        'info_bg': 'bg-primary',
        'info_icon': 'fas fa-boxes',
        'info_text': 'Total Products'
    }


@register.inclusion_tag('adminlte/comp/info_card.html')
def total_users(**kwargs):
    try:
        user_count = Account.objects.all().count()
    except Exception:
        user_count = 0

    return {
        'info': user_count,
        'info_bg': 'bg-info',
        'info_icon': 'fas fa-users',
        'info_text': 'Total Users'

    }


@register.inclusion_tag('adminlte/comp/info_card.html')
def total_sales(**kwargs):
    sales = 0
    try:
        successful_sales = Order.objects.filter(status="Delivered").aggregate(total_sales=Sum('order_total'))
        sales = successful_sales['total_sales']
    except Exception:
        sales = 0

    if sales == None:
        sales = 0

    return {
        'info': '%.2f' %sales,
        'info_bg': 'bg-success',
        'info_icon': 'fas fa-chart-line',
        'info_text': 'Total Sales'
    }
