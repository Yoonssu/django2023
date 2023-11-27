from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('mypage/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('team/', views.TeamList.as_view()),
    path('team/<int:pk>/', views.TeamDetail.as_view(), name='team_detail'),
    path('recommend/<int:pk>/', views.RecommendView.as_view(), name='recommend'),
]
