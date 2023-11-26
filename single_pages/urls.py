from django.urls import path, include
from . import views

urlpatterns = [
    path('about_we/', views.about_we),
    path('', views.landing),
]