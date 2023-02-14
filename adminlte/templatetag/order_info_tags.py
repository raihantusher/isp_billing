from django import template
from orders.models import Order
from django import template

from orders.models import Order

register = template.Library()


@register.inclusion_tag('adminlte/comp/info_card.html')
def pending_order(**kwargs):
    order_count = Order.objects.filter(status="Pending").count()
    return {
        'info': order_count,
        'info_bg': 'bg-danger',
        'info_icon': 'far fa-clock',
        'info_text': 'Pending Orders'
    }


@register.inclusion_tag('adminlte/comp/info_card.html')
def approved_order(**kwargs):
    order_count = Order.objects.filter(status="Approved").count()
    return {
        'info': order_count,
        'info_bg': 'bg-warning',
        'info_icon': 'far fa-check-circle',
        'info_text': 'Approved Orders'
    }


@register.inclusion_tag('adminlte/comp/info_card.html')
def shipped_order(**kwargs):
    order_count = Order.objects.filter(status="Shipped").count()
    return {
        'info': order_count,
        'info_bg': 'bg-primary',
        'info_icon': 'fas fa-dolly',
        'info_text': 'Shipped Orders'
    }


@register.inclusion_tag('adminlte/comp/info_card.html')
def delivered_order(**kwargs):
    order_count = Order.objects.filter(status="Delivered").count()
    return {
        'info': order_count,
        'info_bg': 'bg-success',
        'info_icon': 'fas fa-truck',
        'info_text': 'Delivered Orders'
    }
