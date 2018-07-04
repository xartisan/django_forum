from django.urls import path

from forum.views import PostDetailView, CommentCreateView, CommentListView, CreatePostView, post_like, comment_like
from .views import PostListView

app_name = 'forum'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<uuid:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/add/', CreatePostView.as_view(), name='post_create'),
    path('topic/<uuid:topic_id>/', PostListView.as_view(), name='topic_posts'),
    path(
        'post/<uuid:post_id>/comment/',
        CommentListView.as_view(),
        name='comment_list'),
    path('comment/add/', CommentCreateView.as_view(), name='comment_create'),
    path('post/like', post_like, name='post_like'),
    path('comment/like', comment_like, name='comment_like'),
]
