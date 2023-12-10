from audioop import reverse

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from .models import Post, User, Team, Major, Keyword , Comment, Scrap
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
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# ------------------------------------------------------------------------------------->
class PostList(ListView):
    model = Post
    template_name = 'community/post_list.html'
    context_object_name = 'post_list'
    paginate_by = 10  # 페이지당 post 10개 반환
    
# -----교내/대외/전체 필터링------------------------------------------>
    def get_queryset(self):
        filter_value = self.request.GET.get('filter', 'all')

        if filter_value == 'isduksung':
            return Post.objects.filter(isduksung=True).order_by('-time')
        elif filter_value == 'notIsduksung':
            return Post.objects.filter(isduksung=False).order_by('-time')
        else:
            return Post.objects.all().order_by('-time')
        
# -----페이지네이션---------------------------------------------------->
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)

        paginator = context['paginator']
        page = context['page_obj']
        is_paginated = context['is_paginated']

        try:
            current_page = int(self.request.GET.get('page', 1))
        except ValueError:
            current_page = 1

        max_pages = 5  # 페이지당 페이징 버튼 수
        start_page = max(1, current_page - ((current_page - 1) % max_pages))
        end_page = min(start_page + max_pages - 1, paginator.num_pages)
        page_range = range(start_page, end_page + 1)

        context.update({
            'page_range': page_range,
        })

        try:
            previous_page = page.previous_page_number()
        except EmptyPage:
            previous_page = None

        try:
            next_page = page.next_page_number()
        except EmptyPage:
            next_page = None

        context.update({
            'previous_page': previous_page,
            'next_page': next_page,
            'first_page': 1,
            'last_page': paginator.num_pages,
            'filter_value': self.request.GET.get('filter', 'all'),
        })
        
        return context

# ------------------------------------------------------------------------------------------->

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        return context
    
# ------------------------------------------------------------------------------------------->

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

        selected_images = Recommend.get_dukse_images()

        context.update({
            'selected_images': selected_images,
        })

        return context
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        
        # 로그인한 사용자와 조회하려는 사용자가 다를 경우 404 에러 반환
        if obj != self.request.user:
            raise Http404("You don't have permission to access this page")
        
        return obj
    
    def cancel_scrap(request):
        post_id = request.GET.get('postId')
        post = get_object_or_404(Post, pk=post_id)
        user = request.user

        Scrap.objects.filter(user=user, post=post).delete()
        return JsonResponse({'message': 'Success'})
    
    def delete_team(request):
        post_id = request.GET.get('postId')
        post = get_object_or_404(Post, pk=post_id)
        user = request.user
        Team.objects.filter(user=user, post=post).delete()
        return JsonResponse({'message': 'Success'})
                
    
    
# 키워드 수정 페이지로 이동   
def modKeyWord(request, pk):
    user = User.objects.get(id=pk)
    if request.user != user:
        raise Http404("You don't have permission to access this page")

    return render(
        request,
        'community/modKeyword.html',
    )

# 카테고리에 맞는 키워드 가져오기
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

# 디폴트 키워드 & 사용자가 입력한 키워드 저장하기
def save_keywords(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user.keyword.clear()

        make_keywords = request.POST.get('make_keywords').split(',')
        default_keywords = request.POST.get('default_keywords').split(',')

        for dk in default_keywords:
            if dk.strip() != '':
                try:
                    default_keywords_obj = Keyword.objects.get(keywordname=dk)
                    user.keyword.add(default_keywords_obj.id)
                except Keyword.DoesNotExist:
                    raise Http404("원하는 키워드를 찾을 수 없습니다.")

        for mk in make_keywords:
            if mk.strip() != '':
                try:
                    make_keyword_obj, created = Keyword.objects.get_or_create(keywordname=mk, defaults={'ismake': True, 'category': None})
                    user.keyword.add(make_keyword_obj.id)
                except Keyword.DoesNotExist:
                    new_keyword = Keyword.objects.create(keywordname=mk, ismake=True, category=None)
                    user.keyword.add(new_keyword.id)


        return redirect('community:user_detail', pk=pk)
    
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    

# 관심전공 수정 페이지로 이동
def modMajor(request, pk):
    majors = Major.objects.all()
    user = User.objects.get(id=pk)
    user_major = user.major.all()

    if request.user != user:
        raise Http404("You don't have permission to access this page")


    return render(
        request,
        'community/modMajor.html',
        {
            'majors' : majors,
            'user_major' : user_major,
        }
    )

# 관심전공 저장하기
def save_majors(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.major.clear()

        selected_majors = request.POST.getlist('majors[]')
        for major_id in selected_majors:
            user.major.add(major_id)

        return redirect('community:user_detail', pk=pk)
    
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

# 내가 쓴 글 페이지로 이동
def myTeam(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
        raise Http404("You don't have permission to access this page")

    try:
        teams = Team.objects.filter(user=user)
    except Team.DoesNotExist:
        teams = None

    return render(
        request,
        'community/my_team.html',
        {
            'user' : user,
            'teams' : teams,
        }
    )

# 내가 쓴 댓글 페이지로 이동
def myComment(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
        raise Http404("You don't have permission to access this page")

    try:
        comments = Comment.objects.filter(user=user)
    except Team.DoesNotExist:
        comments = None

    return render(
        request,
        'community/my_team_comment.html',
        {
            'user' : user,
            'comments' : comments,
        }
    )


    


# 바뀐 user를 보고  바꾸는 test
class Recommend(LoginRequiredMixin, ListView):
    model = User
    template_name = 'community/recommend_list.html'
    ordering = '-pk'

    @classmethod
    def get_dukse_images(cls):
        dukse_images_path = os.path.join('community', 'static', 'community', 'dukse')
        dukse_images = [f for f in os.listdir(dukse_images_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
        selected_images = [choice(dukse_images) for _ in range(8)]

        return selected_images

    def get_context_data(self, **kwargs):
        context = super(Recommend, self).get_context_data(**kwargs)

        # 현재 로그인된 사용자의 정보 가져오기
        current_user = self.request.user

        #-----------------------추천 posts-----------------------------
        # 사용자가 선택한 키워드에 맞는 게시글 10개 가져오기
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

        # 상위 8개 포스트 선택
        selected_posts = unique_posts[:8]

        #-----------------------덕새 사진 사져오기-----------------------------
        selected_images = Recommend.get_dukse_images()




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
    template_name = 'community/team_list.html'
    context_object_name = 'team_list'  # 템플릿에서 사용할 컨텍스트 객체의 이름 설정
    paginate_by = 10  # 페이지당 보여질 항목 수

    def get_queryset(self):
        return Team.objects.all()

    def get_context_data(self, **kwargs):
        context = super(TeamList, self).get_context_data(**kwargs)

        # 페이징 처리를 위한 추가적인 컨텍스트 데이터 설정
        paginator = context['paginator']
        page = context['page_obj']

        # 추가 페이징을 위한 컨텍스트 데이터 설정
        context.update({
            'filter_value': self.request.GET.get('filter', 'all'),  # 필터값 추가
        })

        # 새로운 변수 'team_list_number'를 만들어 각 팀 게시글의 전체 목록에서의 순서를 나타냅니다.
        team_list_number = range(context['team_list'].count(), 0, -1)

        # 새로운 변수를 컨텍스트에 추가
        context.update({
            'team_list_number': team_list_number,
        })

        # 페이징 버튼 수 제한을 위한 추가 작업
        try:
            current_page = int(self.request.GET.get('page', 1))
        except ValueError:
            current_page = 1

        max_pages = 5  # 페이지당 최대 페이징 버튼 수
        page_range = []

        if paginator.num_pages <= max_pages:
            page_range = range(1, paginator.num_pages + 1)
        else:
            start_page = max(1, current_page - max_pages // 2)
            end_page = min(paginator.num_pages, start_page + max_pages - 1)
            page_range = range(start_page, end_page + 1)

        context.update({
            'page_range': page_range,
        })

        # 이전 페이지 및 다음 페이지 설정
        previous_page = page.previous_page_number() if page.has_previous() else None
        next_page = page.next_page_number() if page.has_next() else None

        context.update({
            'previous_page': previous_page,
            'next_page': next_page,
        })

        # 맨 처음과 맨 끝 페이지 설정
        context.update({
            'first_page': 1,
            'last_page': paginator.num_pages,
        })

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
        comment_form = CommentForm(user=self.request.user)

        context['comments'] = comments
        context['comment_form'] = comment_form

        return context
    
    def get_absolute_url(self):
        return f'/community/team/{self.object.pk}/'

class TeamPostForm(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamPostForm
    template_name = 'community/team_post_form.html'
    # 글 작성 후 team_list로 이동하는 대신, 아래 함수에서 동적 경로 설정으로 변경 #

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        # JavaScript에서 추가한 post_id를 가져오기
        post_id = self.request.POST.get('post_id')
        kwargs['post_id'] = post_id

        return kwargs

    def form_valid(self, form):
        current_user = self.request.user

        if current_user.is_authenticated:
            form.instance.user = current_user

            # post 필드에서 post_instance를 직접 가져오기
            post_instance = form.cleaned_data['post']

            # Team 객체 생성 및 post 필드에 post_instance 할당
            team_instance = form.save(commit=False)
            team_instance.post = post_instance
            team_instance.save()
            
            # 수정한 부분=> team_list 대신, 해당 post_id의 팀모집게시판으로 가기
            self.success_url = reverse_lazy('community:post_team', kwargs={'pk': post_instance.pk})

            return super().form_valid(form)
        else:
            # 인증되지 않은 사용자에 대한 처리 (예: 리디렉션)
            return redirect('/community')




def new_comment(request, pk):
    if request.user.is_authenticated:
        team = get_object_or_404(Team, pk=pk)

        if request.method == 'POST':
            # CommentForm을 사용할 때 사용자 정보를 함께 전달
            comment_form = CommentForm(data=request.POST, user=request.user)

            if comment_form.is_valid():
                # CommentForm의 save 메서드를 사용하여 댓글을 저장
                comment = comment_form.save(commit=False)
                comment.team = team
                comment.user = request.user
                comment.save()

                return redirect(comment.get_absolute_url())
            else:
                return redirect(team.get_absolute_url())
        else:
            # GET 요청 시에도 CommentForm을 생성할 때 사용자 정보를 함께 전달
            comment_form = CommentForm(user=request.user)

        context = {
            'team': team,
            'comment_form': comment_form,
        }
        return render(request, 'team_detail.html', context)
    else:
        # 사용자가 인증되지 않은 경우 로그인 페이지로 리다이렉트
        return redirect("login")

#-------회원가입 -------------------------------------------------->
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save() 
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user) 
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'community/signup.html', {'form': form})



# ------페이지 로드 시 유저의 스크랩 유무 확인---------------------->
def check_scrap_status(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    is_scraped = Scrap.objects.filter(user=user, post=post).exists()
    return JsonResponse({'is_scraped': is_scraped})


# ------스크랩 버튼 클릭 시 비동기 화면 처리------------------------>
def toggle_scrap(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    scrapped = Scrap.objects.filter(user=user, post=post).exists()

    if scrapped:
        Scrap.objects.filter(user=user, post=post).delete()
        is_scraped = False
    else:
        Scrap.objects.create(user=user, post=post)
        is_scraped = True

    return JsonResponse({'scrapped': is_scraped})


def post_team(request, pk):
    post = get_object_or_404(Post, pk=pk)
    teams_related_to_post = post.get_related_teams()
    return render(request, 'community/post_team.html', {'post': post, 'teams_related_to_post': teams_related_to_post})
    

def search(request):
    query = request.GET.get('q')  # 폼에서 전달된 검색어 가져오기
    results = []

    if query:
        results = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-time')
    # 전체 게시물을 가져오기
    all_posts = Post.objects.all()

    return render(request, 'community/search_result.html', {'results': results, 'all_posts': all_posts, 'query': query})
