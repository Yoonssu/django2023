from audioop import reverse

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    major = models.ManyToManyField('Major', related_name='users')
    keyword = models.ManyToManyField('Keyword', related_name='users')
    email = models.EmailField(unique=True)
    def __str__(self):
        return f'[{self.pk}]{self.username}'

class Keyword(models.Model):
    id = models.BigAutoField(primary_key=True)
    keywordname = models.CharField(max_length=255)
    ismake = models.BooleanField()
    category = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f'{self.keywordname}'
    

class Major(models.Model):
    id = models.BigAutoField(primary_key=True)
    majorname = models.CharField(max_length=255)
    line = models.CharField(max_length=255, null=True, default=None)
    def __str__(self):
        return f'{self.majorname}'

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    img = models.TextField(null=True)
    time = models.DateTimeField(auto_now_add = True)
    isduksung = models.BooleanField()
    def __str__(self):
        return f'[{self.pk}]{self.title}'
    
    def get_absolute_url(self):
        pass

    def get_related_teams(self):
        teams = Team.objects.filter(post=self)
        print(f'Related Teams for Post [{self.pk}]: {teams}')
        return teams

class Scrap(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return f'Scrap [{self.pk}] - {self.post.title} by {self.user.username}'

class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='teams')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.user}'

    def get_absolute_url(self):
        return f'/team/{self.pk}/'

    class Meta:
        ordering = ['-time']  # 최신 객체가 먼저 나오도록 설정
<<<<<<< HEAD

=======
>>>>>>> 773ac712d4b9e9e13d0a61646309fd1ba1ac0f4e

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add = True)
    issecret = models.BooleanField()

    def __str__(self):
        if self.user and hasattr(self.user, 'username'):
            return f'Comment [{self.pk}] on "{self.team.post.title}" by {self.user.username}'
        elif self.user:
            return f'Comment [{self.pk}] on "{self.team.post.title}" by Anonymous User'
        else:
            return f'Comment [{self.pk}] on "{self.team.post.title}" by Unknown User'

    def get_absolute_url(self):
        # 댓글이 추가된 팀의 URL을 반환
        return f'/community{self.team.get_absolute_url()}#comment-{self.pk}'