from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import signup
from .views import new_comment

app_name = 'community'


urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('mypage/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('mypage/<int:pk>/modKeyword/', views.modKeyWord, name='modKeyword'),
    path('mypage/modKeyword/keywords/', views.get_keywords, name='get_keywords'),
    path('mypage/<int:pk>/modMajor/', views.modMajor, name='modMajor'),
    path('team/', views.TeamList.as_view(), name='team_list'),
    path('<int:pk>/new_comment/', views.new_comment, name='new_comment'),
    path('team/<int:pk>/', views.TeamDetail.as_view(), name='team_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='community/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('recommend/<int:pk>/', views.Recommend.as_view(), name='recommend'),
    path('team_post/', views.TeamPostForm.as_view(template_name='community/team_post_form.html'), name="TeamPostForm"),

]