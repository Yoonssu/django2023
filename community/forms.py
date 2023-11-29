from django import forms
from django.contrib.auth.forms import UserCreationForm
from community.models import User  # community 앱의 User 모델을 import

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
