from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView

from common.utils import render_comments_dict, build_comments_dict, ajax_required
from forum.forms import CommentForm, PostForm
from forum.models import Comment
from .models import Post, Topic


class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = 15

    def get_queryset(self):
        qs = Post.published.all()
        topic = Topic.objects.filter(id=self.kwargs.get('topic_id')).first()
        if topic is not None and topic.position != 1:
            qs = qs.filter(topic_id=topic.id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'topics':
                Topic.menu_topics.all(),
            'topic_obj':
                Topic.objects.filter(id=self.kwargs.get('topic_id')).first()
                or Topic.objects.get(position=1),
        })
        return ctx


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'


class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentForm

    # def get_initial(self):
    #     return {
    #         'author': self.request.user.id,
    #     }

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return HttpResponse('OK')

    def form_invalid(self, form):
        return HttpResponse('')


class CommentListView(ListView):
    context_object_name = 'comments'

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.active_comments.filter(post_id=post_id).select_related()

    def get_context_data(self, **kwargs):
        ctx = super(CommentListView, self).get_context_data(**kwargs)
        comments = list(ctx.get('comments'))
        comments.sort(key=lambda x: x.created)
        comments_str = render_comments_dict(build_comments_dict(comments), self.request.user)
        ctx['comments_str'] = comments_str
        return ctx

    def render_to_response(self, context, **response_kwargs):
        comments_str = context['comments_str']
        return HttpResponse(comments_str)


class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'forum/post_form.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        ctx = super(CreatePostView, self).get_context_data(**kwargs)
        topics = Topic.objects.all()
        ctx.update({'topics': topics})
        return ctx

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@ajax_required
@login_required
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.published.get(id=post_id)
            # print(post)
            # print(post.users_like)
            # print(request.user.posts_liked)
            if action == 'like':
                post.users_like.add(request.user)
            elif action == 'unlike':
                post.users_like.remove(request.user)
            post.total_likes = post.users_like.count()
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@ajax_required
@login_required
@require_POST
def comment_like(request):
    comment_id = request.POST.get('id')
    action = request.POST.get('action')

    if comment_id and action:
        try:
            comment = Comment.active_comments.get(id=comment_id)
            if action == 'like':
                comment.users_like.add(request.user)
            elif action == 'unlike':
                comment.users_like.remove(request.user)
            comment.total_likes = comment.users_like.count()
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})
