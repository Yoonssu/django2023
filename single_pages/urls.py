from django.urls import path
from . import views
from community.views import *
from django.contrib.auth import views as auth_views

#app_name = 'single'

urlpatterns = [
    path('about_we/', views.about_we),
    path('', views.landing),
    # path('user_detail/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('recommend/<int:pk>/', views.Recommend.as_view(), name='recommend'),
    # path('community/signup/', views.signup, name='signup'),
    # path('community/login/', auth_views.LoginView.as_view(template_name='community/login.html'), name='login'),
    # path('community/logout/', auth_views.LogoutView.as_view(), name='logout'),
]