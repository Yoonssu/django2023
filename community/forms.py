from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect

from community.models import User, Comment, Post, Team  # community 앱의 User 모델을 import + Comment , Post 모델도

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")


class TeamPostForm(forms.ModelForm):
    post = forms.ModelChoiceField(
        queryset=Post.objects.all(),
        empty_label=None,
        to_field_name='title'
    )

    class Meta:
        model = Team
        fields = ['title', 'content', 'post']

    def __init__(self, user, *args, **kwargs):
        super(TeamPostForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super().save(commit=False)
        current_user = self.user
        if current_user.is_authenticated:
            post_title_instance = self.cleaned_data['post']

            # 괄호 안의 내용을 제거하는 방식
            import re
            cleaned_post_title = re.sub(r'\[\d+\]', '', str(post_title_instance)).strip()

            try:
                post_instance = Post.objects.get(title=cleaned_post_title)
                instance.post = post_instance

                instance.user = current_user
                if commit:
                    instance.save()
                return instance
            except Post.DoesNotExist:
                # Post 객체를 찾을 수 없는 경우
                return None
        else:
            # 인증되지 않은 사용자에 대한 처리 (예: 리디렉션)
            return redirect('/community')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'issecret')
        widgets = {
            'issecret': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }





