from django.contrib.auth.views import LoginView
from django.urls import path

from account.views import register, user_logout

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', user_logout, name='logout'),
]
