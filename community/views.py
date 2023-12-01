from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, User, Team, Major, Keyword
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.db.models import Q 
import operator 
from .forms import UserForm
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
import operator 
from random import sample
from collections import Counter


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

# 바뀐 user를 보고  바꾸는 test
class Recommend(LoginRequiredMixin, ListView):
    model = User
    template_name = 'community/recommend_list.html'
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(Recommend, self).get_context_data(**kwargs)

        # 현재 로그인된 사용자의 정보 가져오기
        current_user = self.request.user

        # 사용자가 선택한 키워드에 맞는 게시글 3개 가져오기
        selected_keywords = current_user.keyword.all()

        # 각각 3개씩 나오게는 성공
        test_posts_dic = {}
        for keyword in selected_keywords:
            test_posts = Post.objects.filter(Q(title__icontains=keyword.keywordname) | Q(content__icontains=keyword.keywordname)).order_by('-time')[:5]
            test_posts_dic[keyword] = test_posts
        
        all_posts_list = []
        for posts in test_posts_dic.values():
            all_posts_list.extend(posts)

        list_len = len(all_posts_list)

        # 중복된 포스트 찾아 중복 횟수 기록
        post_counts = Counter(all_posts_list)

        # 중복 횟수에 따라 정렬하되, 중복 횟수가 같으면 랜덤으로 섞기
        sorted_posts = sorted(all_posts_list, key=lambda post: (post_counts[post], hash(post)), reverse=True)

        # 상위 3개 포스트 선택
        selected_posts = sample(sorted_posts, 3)

        # 사용자가 선택한 전공에 맞는 게시물들 가져오기
        selected_majors = current_user.major.all()
        major_posts = {}
        for major in selected_majors:
            posts = Post.objects.filter(major=major)
            major_posts[major] = posts

        major_list = list(major_posts.keys())
        
        context.update({
            'user': current_user,
            'selected_keywords': selected_keywords,
            'test_posts_dic': test_posts_dic,
            # 'recommended_posts': recommended_posts,
            'list_len': list_len,
            'selected_posts': selected_posts,
            'major_posts': major_posts,
            'major_list': major_list,
        })


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
    
