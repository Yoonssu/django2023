from audioop import reverse

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms
from .models import Post, User, Team, Major, Keyword, Comment
from django.db.models import Count
from .forms import UserForm, CommentForm, TeamPostForm
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from django.db.models import Q 
from functools import reduce
import operator
from django.core.exceptions import PermissionDenied


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

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.user = current_user
            post_title_instance = form.cleaned_data['post']

            print(f"Selected post title: {post_title_instance}")

            # 사용자가 선택한 게시물이 존재하는지 확인
            post_instance = get_object_or_404(Post, title=post_title_instance)

            form.instance.post = post_instance
            return super(TeamPostForm, self).form_valid(form)
        else:
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
    
class Recommend(LoginRequiredMixin, ListView):
    model = User
    template_name = 'community/recommend_list.html'

    def get_context_data(self, **kwargs):
        context = super(Recommend, self).get_context_data(**kwargs)

        # 현재 로그인된 사용자의 정보 가져오기
        current_user = self.request.user

        # 사용자가 선택한 키워드에 맞는 게시글 3개 가져오기
        selected_keywords = current_user.keyword.all()

        # 여러 키워드에 대해 OR 연산을 수행하여 하나 이상의 키워드가 제목 또는 내용에 포함된 게시물을 찾습니다.
        # recommended_posts = Post.objects.filter(
        #     reduce(
        #         operator.or_,
        #         (Q(title__icontains=keyword.keywordname) | Q(content__icontains=keyword.keywordname) for keyword in selected_keywords)
        #     )
        # ).order_by('-time')

        # 각각 3개씩 나오게는 성공
        test_posts_dic = {}
        for keyword in selected_keywords:
            test_posts = Post.objects.filter(Q(title__icontains=keyword.keywordname) | Q(content__icontains=keyword.keywordname)).order_by('-time')[:3]
            test_posts_dic[keyword] = test_posts

        # 사용자가 선택한 전공에 맞는 게시물들 가져오기
        selected_majors = current_user.major.all()
        major_posts = {}
        for major in selected_majors:
            posts = Post.objects.filter(major=major)
            major_posts[major] = posts

        major_list = list(major_posts.keys())

        context.update({
            'user': current_user,
            # 'recommended_posts': recommended_posts,
            'major_posts': major_posts,
            'major_list': major_list,
            'selected_keywords': selected_keywords,
            'test_posts_dic': test_posts_dic,
        })

        return context
    
