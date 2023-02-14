from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required

from store.models import Article
from adminlte.forms import ArticleForm
from django.contrib.admin.views.decorators import staff_member_required


class ArticleList(ListView):
    model =  Article
    context_object_name = "article_list"
    template_name = 'dashboard/pages/article_list.html'


    def get_queryset(self):
        query = self.request.GET.get("s")
        if query:
            return Article.objects.filter(name__startswith=query)
        else:
            return Article.objects.order_by("-id")

    def get_context_data(self,*args, **kwargs):
        data = super().get_context_data(**kwargs)
        data['page_title'] = 'Authors'
        return data


@staff_member_required
def add_new_article(request):
    article_form = ArticleForm()

    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article_form.save()

    context = {
        'article_form':article_form
    }
    return render(request, 'dashboard/pages/add_new_article.html', context)

@staff_member_required
def edit_article(request, id ):
    article = Article.objects.get(pk=id)
    article_form = ArticleForm(instance=article)

    if request.method == "POST":
        article_form = ArticleForm(instance=article , data=request.POST)
        article.save()
    context = {
        'article_form': article_form
    }
    return render(request, 'dashboard/pages/add_new_article.html', context)

@staff_member_required
def delete_article(request, id):
    if request.method == "POST":
        article = Article.objects.get(pk=id)
        article.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))