from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, User, Team, Keyword
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

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
    template_name = 'user/user_detail.html'  # 실제 템플릿 파일 경로로 수정

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
    
def modKeyWord(request, pk):
    return render(
        request,
        'user/modKeyword.html',
    )

def get_keywords(request):
    category = request.GET.get('category')

    if category == '1':
        category_keywords = Keyword.objects.filter(category='활동 분야')
    elif category == '2':
        category_keywords = Keyword.objects.filter(category='언론/미디어')
    elif category == '3':
        category_keywords = Keyword.objects.filter(category='디자인/사진/예술/영상')
    elif category == '4':
        category_keywords = Keyword.objects.filter(category='경제/금융')
    elif category == '5':
        category_keywords = Keyword.objects.filter(category='경영/컨설팅')
    elif category == '6':
        category_keywords = Keyword.objects.filter(category='과학/공학/기술/IT')

    keyword_data = {'keywords': list(category_keywords.values())}
    return JsonResponse(keyword_data)

# def get_keywords(request):

#     if category == '1':
#         category_keywords = Keyword.objects.filter(category='활동 분야')
#     elif category == '2':
#         category_keywords = Keyword.objects.filter(category='언론/미디어')
#     elif category == '3':
#         category_keywords = Keyword.objects.filter(category='디자인/사진/예술/영상')
#     elif category == '4':
#         category_keywords = Keyword.objects.filter(category='경제/금융')
#     elif category == '5':
#         category_keywords = Keyword.objects.filter(category='경영/컨설팅')
#     elif category == '6':
#         category_keywords = Keyword.objects.filter(category='과학/공학/기술/IT')

#     data = {'keywords': list(category_keywords.values())}
#     return JsonResponse(data)
    

def modMajor(request, pk):
    return render(
        request,
        'user/modMajor.html',
    )

    
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