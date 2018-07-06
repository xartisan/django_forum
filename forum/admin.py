from django.contrib import admin

from .models import Post, Comment, Topic


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'author', 'publish', 'modified', 'status')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'parent_comment', 'body', 'user')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_top_menu', 'position')
