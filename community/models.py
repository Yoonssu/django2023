from django.db import models

# Create your models here.
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    # userId = models.CharField(max_length=40)
    major = models.ManyToManyField('Major', related_name='users')
    keyword = models.ManyToManyField('Keyword', related_name='users')
    password = models.CharField(max_length=255)
    email = models.EmailField()
    def __str__(self):
        return f'{self.id}'



class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_major = models.BooleanField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    img = models.TextField(null=True)
    time = models.DateTimeField()
    duksung = models.BooleanField()

class Scrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField()
    secret = models.BooleanField()

class Team(models.Model):
    id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    time = models.DateTimeField()

class Major(models.Model):
    id = models.BigAutoField(primary_key=True)
    major = models.CharField(max_length=255)
    def __str__(self):
        return f'{self.major}'

class Keyword(models.Model):
    id = models.BigAutoField(primary_key=True)
    label = models.CharField(max_length=255)
    is_make = models.BooleanField()
    category = models.CharField(max_length=255, null=True)
    def __str__(self):
        return f'{self.label}'
