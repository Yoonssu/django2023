from django.urls import path
from . import views
from community.views import *
from django.contrib.auth import views as auth_views
from .views import search

#app_name = 'single'

urlpatterns = [
    path('about_we/', views.about_we),
    path('', views.landing),
    path('search/', views.search, name='search'),
    
    # path('community/signup/', views.signup, name='signup'),
    # path('community/login/', auth_views.LoginView.as_view(template_name='community/login.html'), name='login'),
    # path('community/logout/', auth_views.LogoutView.as_view(), name='logout'),
]