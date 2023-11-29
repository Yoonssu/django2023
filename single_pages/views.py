from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView
from community.models import *
from community.views import *
from community.forms import UserForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count

# Create your views here.
def landing(request):
    return render(
        request,
        'single_pages/landing.html'
    )


def about_we(request):
    return render(
        request,
        'single_pages/about_we.html'
    )


