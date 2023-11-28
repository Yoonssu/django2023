from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, User, Team, Major, Keyword
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.db.models import Q 
from functools import reduce
import operator 

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
    template_name = 'community/user_detail.html'  

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        
        # 여기에서 유저의 관심전공, 맞춤 키워드, 스크랩한 활동 등을 가져와 context에 추가
        user = self.object

        # 예시: 유저의 관심전공 목록
        majors = user.major.all()
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
