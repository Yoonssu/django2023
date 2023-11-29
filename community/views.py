from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, User, Team, Major, Keyword
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.db.models import Q 
from functools import reduce
import operator 
from .forms import UserForm
from django.contrib.auth import authenticate,login


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



def recommend(request, pk):
    user = get_object_or_404(User, pk=pk)

    # 사용자가 선택한 키워드에 맞는 게시글 3개 가져오기(제가 임의로 최신 3개라는 추천 로직을 쓴 거고, 실제 로직을 이 틀에서 변형해서 구현하셔야 해요 )
    selected_keywords = user.keyword.all()

    # 여러 키워드에 대해 OR 연산을 수행하여 하나 이상의 키워드가 제목 또는 내용에 포함된 게시물을 찾습니다.
    recommended_posts = Post.objects.filter(
        reduce(
            operator.or_,
            (Q(title__icontains=keyword) | Q(content__icontains=keyword) for keyword in selected_keywords)
        )
    ).order_by('-time')


    #각각 3개씩 나오게는 성공
    test_posts_dic = {}
    for keyword in selected_keywords:
        test_posts = Post.objects.filter(Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by('-time')[:3]
        test_posts_dic[keyword] = test_posts


    # 사용자가 선택한 전공에 맞는 게시물들 가져오기
    selected_majors = user.major.all()
    major_posts = {}
    for major in selected_majors:
        posts = Post.objects.filter(major=major)
        major_posts[major] = posts
    
    major_list = list(major_posts.keys())

    context = {
        'user': user,
        # 'recommended_posts': recommended_posts,
        'major_posts': major_posts,
        'major_list': major_list,
        'selected_keywords': selected_keywords,
        # 'test_posts': test_posts,
        "test_posts_dic": test_posts_dic,
    }

    return render(request, 'community/recommend.html', context)

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

