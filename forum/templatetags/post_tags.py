from django import template
from django.db.models import Count
from django.utils import timezone
from taggit.models import Tag

from forum.models import Topic
from ..models import Post

register = template.Library()


@register.simple_tag
def menu_topics():
    return Topic.menu_topics.all()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    q = Post.published.annotate(
        total_comments=Count('comments')).order_by('-total_comments')
    return q[:count]


@register.simple_tag
def archives():
    return Post.published.dates('publish', 'month', order='DESC')[:]


@register.simple_tag
def all_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    request = context['request']
    updated = request.GET.copy()
    for k, v in kwargs.items():
        updated[k] = v
    return updated.urlencode()


@register.filter
def pretty_date(publish_date):
    now = timezone.now()
    time_diff = now - publish_date

    if time_diff.days > 0:
        return str(time_diff.days) + '天前'

    total_seconds = time_diff.total_seconds()
    if total_seconds > 3600:
        return str(int(total_seconds) // 3600) + '小时前'
    if total_seconds > 60:
        return str(int(total_seconds) // 60) + '分钟前'
    return '刚刚'
