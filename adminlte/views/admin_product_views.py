import json

from django.contrib import messages
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView

from adminlte.forms import ProductForm
from store.models import Product, ProductGallery, Variation
from django.contrib.admin.views.decorators import staff_member_required

class ProductList(ListView):
    model = Product
    context_object_name = "product_list"
    template_name = 'dashboard/pages/product_list.html'
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Product.objects.filter(
                Q(product_name__icontains=query) |
                Q(slug__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
        else:
            return Product.objects.order_by("-id")

    # def get_context_data(self, *args, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     data['page_title'] = 'Authors'
    #     return data

@staff_member_required
def add_new_product(request):
    product_form = ProductForm()
    GalleryFormSet = inlineformset_factory(Product, ProductGallery, fields=('image',), max_num=5)
    gallery_form =None
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)

        if product_form.is_valid():
            # print(product_form.errors)
            product = product_form.save()

            gallery_form = GalleryFormSet(request.POST, request.FILES, instance=product)
            if gallery_form.is_valid():
                gallery_form.save()
                print(gallery_form)
            # print(product.id)

            # print(request.POST.keys())
            all_color_variations = request.POST.getlist("color[value]")
            # print(all_variation)
            for color in all_color_variations:
                product.variations.create(variation_category="color",
                                          variation_value=color)  # print(request.POST.keys())

            all_size_variations = request.POST.getlist("size[value]")
            # print(all_variation)
            for size in all_size_variations:
                product.variations.create(variation_category="size", variation_value=size)

            messages.success(request, "Product is added successfully!")
    else:
        gallery_form = GalleryFormSet()

    context = {
        'product_form': product_form,
        'gallery': gallery_form
    }
    return render(request, 'dashboard/pages/add_new_product.html', context)


@staff_member_required
def edit_product(request, id):
    product = Product.objects.get(pk=id)
    product_form = ProductForm(instance=product)
    GalleryFormSet = inlineformset_factory(Product, ProductGallery, fields=('image',), max_num=5)

    if request.method == "POST":
        product_form = ProductForm(instance=product, data=request.POST, files=request.FILES)
        gallery_form = GalleryFormSet(request.POST, request.FILES, instance=product)
        if product_form.is_valid() and gallery_form.is_valid():

            colors = request.POST.getlist("color[value]")
            color_id = request.POST.getlist("color[id]")

            # print(all_variation)
            # for index in range(len(colors)):
            #
            #     if int(color_id[index]) != 0:
            #         print(color_id[index])
            #         current_color = product.variations.get(pk=color_id[index])
            #         current_color.variation_value = colors[index]
            #         current_color.save()
            #     else:
            #         product.variations.create(variation_category="color",
            #                                   variation_value=colors[index])  # print(request.POST.keys())

            all_size_variations = request.POST.getlist("size[value]")
            for size in all_size_variations:
                product.variations.update_or_create(variation_category="size", variation_value=size)

            for color in colors:
                product.variations.update_or_create(variation_category="color", variation_value=color)

            product_form.save()
            gallery_form.save()
    else:
        gallery_form = GalleryFormSet(instance=product)

    context = {
        'product_form': product_form,
        'gallery': gallery_form,
        'product_id': id
    }
    return render(request, 'dashboard/pages/edit_product.html', context)

@staff_member_required
def delete_product(request, id):
    if request.method == "POST":
        product = Product.objects.get(pk=id)
        imgs = ProductGallery.objects.filter(product=product)

        for img in imgs:
            img.delete()

        product.delete()
        messages.success(request, 'Product is deleted successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# retrieve variations
@staff_member_required
def product_colors(request, product_id):
    single_product = Product.objects.get(pk=product_id)

    li = []
    for i in single_product.variations.all_colors():
        # print(i.variation_value)
        color = {'id': i.id, 'color': i.variation_value, 'is_active': i.is_active}
        li.append(color)

    return JsonResponse({
        'colors': li
    })

@staff_member_required
def product_sizes(request, product_id):
    single_product = Product.objects.get(pk=product_id)

    li = []
    for i in single_product.variations.all_sizes():
        # print(i.variation_value)
        size = {'id': i.id, 'size': i.variation_value, 'is_active': i.is_active}
        li.append(size)

    return JsonResponse({
        'sizes': li
    })


@staff_member_required
def delete_variation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data["id"]
        variation = Variation.objects.get(pk=uid)
        if variation.delete():
            return JsonResponse({
                'deleted': True
            })

    return JsonResponse({
        "deleted": False
    })

@staff_member_required
def update_variation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        uid = data["id"]
        variation = Variation.objects.get(pk=uid)
        variation.is_active = not variation.is_active
        variation.save()

        return JsonResponse({
            'updated': True
        })

    return JsonResponse({
        "updated": False
    })
