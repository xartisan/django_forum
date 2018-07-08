from django.urls import path

from chatroom import views

app_name = 'chatroom'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('send_msg/', views.send_msg, name='send_msg'),
    path('new_msg/', views.get_msgs, name='get_new_msgs'),
    path('friends_status/', views.check_friends_status, name='check_my_friends_status'),
    path('upload/', views.upload_file, name='upload_file'),
    path('upload_file_progress/', views.upload_file_progress, name='upload_file_progress'),
    path('delete_cache_key/', views.delete_key, name='delete_cache_key'),
]
