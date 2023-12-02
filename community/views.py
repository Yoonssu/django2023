from audioop import reverse

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from .models import Post, User, Team, Major, Keyword , Comment
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import UserForm, CommentForm, TeamPostForm
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from functools import reduce
import operator 
from random import random, choice 
from collections import Counter
import os
from django.core.exceptions import PermissionDenied
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

# 바뀐 user를 보고  바꾸는 test
class Recommend(LoginRequiredMixin, ListView):
    model = User
    template_name = 'community/recommend_list.html'
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(Recommend, self).get_context_data(**kwargs)

        # 현재 로그인된 사용자의 정보 가져오기
        current_user = self.request.user

        #-----------------------추천 posts-----------------------------
        # 사용자가 선택한 키워드에 맞는 게시글 3개 가져오기
        selected_keywords = current_user.keyword.all()

        posts_dic = {}
        for keyword in selected_keywords:
            posts = Post.objects.filter(Q(title__icontains=keyword.keywordname) | Q(content__icontains=keyword.keywordname)).order_by('-time')[:10]
            posts_dic[keyword] = posts
        
        all_posts_list = []
        for posts in posts_dic.values():
            all_posts_list.extend(posts)

        # 중복된 포스트 찾아 중복 횟수 기록
        post_counts = Counter(all_posts_list)

        # 중복 횟수에 따라 정렬하되, 중복 횟수가 같으면 랜덤으로 섞기
        sorted_posts = sorted(all_posts_list, key=lambda post: (post_counts[post], random()), reverse=True)

        # 중복된 포스트 중 하나만 유지
        unique_posts = []
        seen_posts = set()

        for post in sorted_posts:
            if post not in seen_posts:
                unique_posts.append(post)
                seen_posts.add(post)

        # 상위 3개 포스트 선택
        selected_posts = unique_posts[:8]

        #-----------------------덕새 사진 사져오기-----------------------------
        # 'community/dukse/' 폴더 내의 모든 이미지 파일 가져오기
        dukse_images_path = os.path.join('community', 'static', 'community', 'dukse')
        dukse_images = [f for f in os.listdir(dukse_images_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

        # selected_images에 랜덤하게 1개 선택하여 8번 반복
        selected_images = [choice(dukse_images) for _ in range(8)]




        #-----------------------전공 posts-----------------------------

        # 사용자가 선택한 전공에 맞는 게시물들 가져오기
        selected_majors = current_user.major.all()
        major_posts = {}
        for major in selected_majors:
            posts = Post.objects.filter(major=major).order_by('-pk')
            major_posts[major] = posts

        all_major_posts_list = []
        for posts in major_posts .values():
            all_major_posts_list.extend(posts)
        all_major_posts_list = sorted(all_major_posts_list, key=lambda post: post.pk, reverse=True)

        major_list = list(major_posts.keys())

        #-----------------------전공 posts 페이징-----------------------------

        # 전체 포스트에 대한 페이징 추가
        paginator_all = Paginator(all_major_posts_list, 10)
        page_all = self.request.GET.get('page_all')

        try:
            all_major_posts_list = paginator_all.page(page_all)
        except PageNotAnInteger:
            all_major_posts_list = paginator_all.page(1)
        except EmptyPage:
            all_major_posts_list = paginator_all.page(paginator_all.num_pages)

        # 각 전공별 포스트에 대한 페이징 추가
        paginator_majors = {}
        page_majors = {}

        for major, posts in major_posts.items():
            paginator_majors[major] = Paginator(posts, 10)
            page_majors[major] = self.request.GET.get(f'page_{major}')

            try:
                major_posts[major] = paginator_majors[major].page(page_majors[major])
            except PageNotAnInteger:
                major_posts[major] = paginator_majors[major].page(1)
            except EmptyPage:
                major_posts[major] = paginator_majors[major].page(paginator_majors[major].num_pages)
        
        context.update({
            'user': current_user,
            'selected_keywords': selected_keywords,
            'posts_dic': posts_dic,
            'selected_posts': selected_posts,
            'major_posts': major_posts,
            'major_list': major_list,
            'all_major_posts_list': all_major_posts_list,
            'selected_images': selected_images,
            'paginator_all': paginator_all,
            'major_posts': major_posts,
            'paginator_majors': paginator_majors,
        })


        return context

class TeamList(ListView):
    model = Team
    template_name = 'community/team_list.html'  # 적절한 템플릿 경로로 변경

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 추가적인 컨텍스트 데이터가 필요하다면 여기에 작성
        return context
    
class TeamDetail(DetailView):
    model = Team
    template_name = 'community/team_detail.html'


    def get_context_data(self, **kwargs):
        context = super(TeamDetail, self).get_context_data(**kwargs)
        team = self.object

        # 댓글 목록 가져오기
        comments = Comment.objects.filter(team=team)

        # 댓글 작성 폼 생성
        comment_form = CommentForm()

        context['comments'] = comments
        context['comment_form'] = comment_form

        return context

class TeamPostForm(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamPostForm  # 사용할 폼 클래스 설정
    success_url = reverse_lazy('community:team_list')
    template_name = 'team_post_form'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # 사용자 정보를 폼에 전달
        return kwargs

    from django.shortcuts import get_object_or_404

    class TeamPostForm(LoginRequiredMixin, CreateView):
        # (이전 코드 생략)

        def form_valid(self, form, post_instance=None):
            current_user = self.request.user
            if current_user.is_authenticated:
                form.instance.user = current_user
                post_title_instance = form.cleaned_data['post']

                # 괄호 안의 pk 번호 제거하고 title 검색해서 Post 객체 가져오기
                import re
                cleaned_post_title = re.sub(r'\[\d+\]', '', str(post_title_instance)).strip()


                # Post 모델에서 해당 title에 매칭되는 객체 가져오기
                # 여러 개의 객체가 반환되더라도 첫 번째 객체만 사용
                post_instance = Post.objects.filter(title=cleaned_post_title).first()

                if post_instance:
                    # Team 객체 생성 및 post 필드에 post_instance 할당
                    team_instance = form.save(commit=False)
                    team_instance.post = post_instance
                    team_instance.save()

                    return super(TeamPostForm, self).form_valid(form)
                else:
                    # 인증된 사용자이지만, post_instance가 없는 경우
                    return None
            else:
                # 인증되지 않은 사용자에 대한 처리 (예: 리디렉션)
                return redirect('/community')


def new_comment(request, pk):
    if request.user.is_authenticated:
        team = get_object_or_404(Team, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.team = team
                comment.author = request.user
                comment.save()

                return redirect(comment.get_absolute_url())

            else:
                return redirect(team.get_absolute_url())
    else:
        # 사용자가 인증되지 않은 경우 로그인 페이지로 리다이렉트
        return redirect("login")



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


def post_team(request, pk):
    post = get_object_or_404(Post, pk=pk)
    teams_related_to_post = post.get_related_teams()
    return render(request, 'community/post_team.html', {'post': post, 'teams_related_to_post': teams_related_to_post})
    