import functools
import json
import os
import time

import redis
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from account.models import UserProfile
from chatroom.models import Group
from forum.models import Topic

r = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def set_status(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        request = args[0]
        status_key = "{}_status".format(request.user.profile.id)
        r.set(status_key, 1, 1000)  # 保存用户在线状态5分钟
        return f(*args, **kwargs)  # 继续执行取消息的方法

    return decorator


@login_required
@set_status
def dashboard(request):
    return render(request, "chatroom/dashboard.html",
                  {'topics': Topic.menu_topics.all()})


@login_required
@set_status
def send_msg(request):
    msg = request.POST.get('data')
    if msg:
        msg = json.loads(msg)
        if msg.get('to'):
            msg_sender = UserProfile.objects.get(id=msg['from'])
            msg['nickname'] = msg_sender.name
            msg['avatar'] = msg_sender.avatar.url
            msg['timestamp'] = time.strftime('%Y:%m:%d-%H:%M:S',
                                             time.localtime(time.time()))
            msg_receiver_list = []
            if msg['type'] == 'single':
                msg_receiver_list = [msg['to']]
            elif msg['type'] == 'group':
                group = Group.objects.get(id=msg['to'])
                msg_receiver_list = [
                    m.id for m in group.members.exclude(request.user.profile)
                ]
            msg_json_str = json.dumps(msg)
            for receiver in msg_receiver_list:
                r.rpush('receiver' + receiver, msg_json_str)
            return JsonResponse({'status', 'ok'})
    return JsonResponse({'status': 'ko'})


@login_required
@set_status
def get_msgs(request):
    msg_list = r.lrange('receiver' + str(request.user.profile.id), 0, -1)
    msg_list = [json.loads(x.decode('utf-8')) for x in msg_list]
    return HttpResponse(json.dumps(msg_list))


@login_required
def check_friends_status(request):
    friends = request.user.profile.friends.select_related()
    online_friends = []
    for friend in friends:
        if r.get('{}_status'.format(friend.id)) is not None:
            online_friends.append(str(friend.id))

    return HttpResponse(json.dumps(online_friends))


@login_required
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        upload_folder = settings.BASE_DIR + '/uploads/{}'.format(request.user.profile.id)
        if not os.path.exists(upload_folder):
            os.mkdir(upload_folder)
        file_path = '{}/{}'.format(upload_folder, file.name)
        recv_size = 0
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
                recv_size += len(chunk)
                r.set(f.name, recv_size)
        return HttpResponse(file_path)
    return render(request, 'chatroom/test.html')


def upload_file_progress(request):
    filename = request.GET.get('filename')
    progress = r.get(filename)
    return JsonResponse(json.dumps({'recv_size': progress}))


def delete_key(request):
    key = request.GET.get('cache_key')
    r.delete(key)
    return HttpResponse({'status': 'ok'})
