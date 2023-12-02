from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import signup
from .views import new_comment
from .views import *

app_name = 'community'


urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('mypage/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('mypage/<int:pk>/modKeyword/', views.modKeyWord, name='modKeyword'),
    path('mypage/modKeyword/keywords/', views.get_keywords, name='get_keywords'),
    path('mypage/<int:pk>/modMajor/', views.modMajor, name='modMajor'),
    path('recommend/<int:pk>/', views.Recommend.as_view(), name='recommend'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='community/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('scrap/<int:post_id>/', views.toggle_scrap, name='toggle_scrap'),

    path('team/', views.TeamList.as_view(), name='team_list'),  # 팀 전체 게시판 url
    path('team/<int:pk>/', views.TeamDetail.as_view(), name='team_detail'),  # 팀 모집글 detail 페이지
    path('team_post/', views.TeamPostForm.as_view(template_name='community/team_post_form.html'), name="TeamPostForm"), #팀 모집글 작성 Form
    path('team/<int:pk>/new_comment/', views.new_comment, name='new_comment'), #팀 모집 댓글 url
    path('<int:pk>/post_team/', views.post_team, name='post_team'), # post에서 해당 팀 모집글 리스트 보기


]

