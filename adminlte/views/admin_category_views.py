from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from category.models import Category
from adminlte.forms import CategoryForm
from django.db.models import Q


class CategoryList(ListView):
    model =  Category
    context_object_name = "category_list"
    template_name = 'dashboard/pages/category_list.html'
    paginate_by = 25


    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Category.objects.filter(
                Q(category_name__icontains=query)
            )
        else:
            return Category.objects.order_by("-id")

    # def get_context_data(self,*args, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     data['page_title'] = 'Authors'
    #     return data


@staff_member_required
def add_new_category(request):
    category_form = CategoryForm()

    if request.method == "POST":
        category_form = CategoryForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, ' Category is created successfully!')
            redirect('category_list')

    context = {
        'category_form':category_form
    }
    return render(request, 'dashboard/pages/add_new_category.html', context)


@staff_member_required
def edit_category(request, id):
    category = Category.objects.get(pk=id) 
    category_form = CategoryForm(instance=category)

    if request.method == "POST":
        category_form = CategoryForm(instance=category, data=request.POST, files=request.FILES)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, f' {category.category_name} category is updated successfully!')
            redirect('category_list')

    context = {
        'category_form':category_form,
        'category' : category
    }
    return render(request, 'dashboard/pages/edit_category.html', context)


@staff_member_required
def delete_category(request, id ):
    if request.method == "POST":
        category = Category.objects.get(pk=id)
        category.delete()
        messages.success(request, f' {category.category_name} category is deleted successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))