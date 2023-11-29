from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, User, Team, Keyword
from django.db.models import Count
from .forms import UserForm
from django.contrib.auth import authenticate,login
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
    

class UserDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/user_detail.html'  # 실제 템플릿 파일 경로로 수정

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        
        # 현재 로그인된 사용자의 정보 가져오기
        current_user = self.request.user

        # 예시: 로그인된 사용자의 관심전공 목록
        context['current_user_majors'] = current_user.major.all()

        # 예시: 로그인된 사용자의 맞춤 키워드 목록
        context['current_user_keywords'] = current_user.keyword.all()

        # 예시: 로그인된 사용자가 스크랩한 활동 목록
        context['current_user_scraps'] = current_user.scrap_set.all()

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

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  # 이 부분에서 모델이 저장됩니다.
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user) #로그인 아직 구현 안했는데..
            # 회원가입 후 'landing' 페이지로 리다이렉션
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'community/signup.html', {'form': form})