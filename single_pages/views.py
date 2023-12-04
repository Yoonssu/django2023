from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from community.models import *
from community.views import *
from community.forms import UserForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models import Q
from django.http import Http404

# Create your views here.
def landing(request):
    return render(
        request,
        'single_pages/landing.html'
    )


def about_we(request):
    return render(
        request,
        'single_pages/about_we.html'
    )


# views.py
from django.shortcuts import render
from community.models import Post  # YourModel은 실제 모델명으로 대체해야 합니다.

def search(request):
    query = request.GET.get('q')  # 폼에서 전달된 검색어 가져오기
    results = []

    if query:
        results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    
    # 전체 게시물을 가져오기
    all_posts = Post.objects.all()

    return render(request, 'community/search_result.html', {'results': results, 'all_posts': all_posts, 'query': query})