from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, User, Team 
from django.db.models import Count
from django.shortcuts import get_object_or_404


# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        return context
    
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        return context
    

class UserDetail(DetailView):
    model = User
    # template_name = 'your_app_name/user_detail.html'  # 실제 템플릿 파일 경로로 수정

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        
        # 여기에서 유저의 관심전공, 맞춤 키워드, 스크랩한 활동 등을 가져와 context에 추가
        user = self.get_object()

        # 예시: 유저의 관심전공 목록
        context['majors'] = user.major.all()

        # 예시: 유저의 맞춤 키워드 목록
        context['keywords'] = user.keyword.all()

        # 예시: 유저가 스크랩한 활동 목록
        context['scraps'] = user.scrap_set.all()

        return context
    
class TeamList(ListView):
    model = Team
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(TeamList, self).get_context_data()
        return context
    
class TeamDetail(DetailView):
    model = Team
    
    def get_context_data(self, **kwargs):
        context = super(TeamDetail, self).get_context_data()
        return context