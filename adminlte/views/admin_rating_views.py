from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required

from store.models import ReviewRating
from store.forms import ReviewForm

from django.contrib.admin.views.decorators import staff_member_required


class RatingList(ListView):
    model = ReviewRating
    context_object_name = "review_rating_list"
    template_name = 'dashboard/pages/review_rating_list.html'
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get("s")
        if query:
            return ReviewRating.objects.filter(name__startswith=query)
        else:
            return ReviewRating.objects.order_by("-id")

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = 'Authors'
        return data

@staff_member_required
def edit_review(request, id):
    review = ReviewRating.objects.get(pk=id)
    review_form = ReviewForm(instance=review)

    if request.method == "POST":
        review_form = ReviewForm(instance=review, data=request.POST, files=request.FILES)
        if review_form.is_valid():
            review_form.save()
            messages.success(request, 'Review is updated successfully!')

    context = {
        'review_form': review_form
    }
    return render(request, 'dashboard/pages/edit_review.html', context)

@staff_member_required
def delete_review(request, id):
    if request.method == "POST":
        review = ReviewRating.objects.get(pk=id)
        review.delete()
        messages.success(request, 'Review is deleted successfully!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
