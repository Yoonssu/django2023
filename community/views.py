from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, User, Team 
from django.db.models import Count
from .forms import UserForm
from django.contrib.auth import authenticate,login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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
    template_name = 'community/user_detail.html'

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







def post_list(request):
    page = request.GET.get('page', 1)
    posts_per_page = 10
    
    if request.GET.get('category') == 'internal':
        post_list = Post.objects.filter(is_duksung=True)
    elif request.GET.get('category') == 'external':
        post_list = Post.objects.filter(is_duksung=False)
    else:
        post_list = Post.objects.all()

    paginator = Paginator(post_list, posts_per_page)

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    context = {'post_list': post_list}
    return render(request, 'community/post_list.html', context)

