from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import signup

from .views import PostListView

app_name = 'community'


urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('mypage/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('team/', views.TeamList.as_view()),
    path('team/<int:pk>/', views.TeamDetail.as_view(), name='team_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='community/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('recommend/<int:pk>/', views.RecommendView.as_view(), name='recommend'),
    #  path('community/', post_list, name='post_list'),
    path('post_list/', PostListView.as_view(), name='post_list'),
]

