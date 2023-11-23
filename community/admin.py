from django.contrib import admin
from .models import User, Post, Comment, Team, Major, Keyword, Scrap

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Team)
admin.site.register(Major)
admin.site.register(Keyword)
admin.site.register(Scrap)

