from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'body')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'body', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('body',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')
    list_filter = ('post', 'user')

# Register your models here.
