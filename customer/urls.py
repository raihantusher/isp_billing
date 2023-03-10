from django.urls import path

from .views import CustomerList

urlpatterns = [
 path('list/', CustomerList.as_view(), name="customer_list" ),

]