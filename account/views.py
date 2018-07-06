from django.contrib.auth.views import logout
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse

from account.forms import RegistrationForm
from account.models import UserProfile


def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        cd = form.cleaned_data
        user = form.save(commit=False)
        user.set_password(cd['password'])
        user.save()
        UserProfile.objects.create(user=user)
        return render(request, 'account/register_done.html', {'new_user': user})

    ctx = {'form': form}
    return render(request, 'account/register.html', context=ctx)


def user_logout(request):
    logout(request)
    return redirect(reverse('forum:post_list'))
