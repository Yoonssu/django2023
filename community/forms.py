from django import forms
from django.contrib.auth.forms import UserCreationForm
from community.models import User, Comment, Post  # community 앱의 User 모델을 import + Comment , Post 모델도

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")


class TeamPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'issecret')
        widgets = {
            'issecret': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }





