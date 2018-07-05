import functools
from collections import OrderedDict

from django.http import HttpResponseBadRequest
from django.utils import timezone


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


def build_comments_dict(comments):
    """
    :param comments: sorted list of comments
    :return nested comment tree
    """
    rv = OrderedDict()
    record = {None: rv}

    for comment in comments:
        subs = OrderedDict()
        record[comment.parent_comment][comment] = subs
        record[comment] = subs

    return rv


def render_comments_dict(comments, current_user):
    if not comments:
        return ""
    rv = ""
    template = """\
    <div class="media">
        <div class="media-left">
            <a href="{0}" class="comment-head-img">
                <img class="media-object comment-head-img" src="{2}" alt="{3}的头像">
            </a>
        </div>
        <div class="media-body">
            <h4 class="media-heading">{3}<small class="margin-left-twenty">{4}</small>
            <small class='comment-bar pull-right'>
            <a style='cursor: pointer' data-id="{1}" data-action="{6}"  class='margin-left-twenty' comment-type='2'>
            <i {8} class='fa fa-thumbs-o-up fa-fw'></i>
            {7}</a>
            <a style='cursor: pointer' data-id="{1}" class='margin-left-twenty' comment-type='1'>回复</a>
            </small>
            </h4>
            <p>{5}</p>\
    """
    for comment in comments:
        current_user_liked = current_user in comment.users_like.all()
        elem = template.format(comment.user.id, comment.id,
                               comment.user.profile.avatar.url,
                               comment.user.profile.name, pretty_date(comment.created), comment.body,
                               'unlike' if current_user_liked else 'like', comment.total_likes,
                               'style="color: red"' if current_user_liked else '')
        elem += render_comments_dict(comments[comment], current_user)
        elem += "</div></div>"
        rv += elem

    return rv


def ajax_required(f):
    @functools.wraps(f)
    def decorator(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    return decorator
