import csv

from django.http import HttpResponse

from orders.models import OrderProduct
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def report(request, year):
    # csv headers
    response = HttpResponse(
        content_type='text/csv',

    )
    response['Content-Disposition'] = ' attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    # csv headers

    order_products = OrderProduct.objects \
        .filter(created_at__year=year) \
        .select_related('product') \
        .select_related('user') \
        .select_related('order')

    for op in order_products:
        print(op.user)
        print(op.product)
        print(op.order.created_at)

    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
