from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from forum.models import Comment, Post, Topic

User = get_user_model()


class CommentForm(ModelForm):
    # post = forms.ModelChoiceField(
    #     widget=forms.HiddenInput,
    #     queryset=Post.published.all(),
    #     disabled=True,
    #     required=False,
    # )
    # author = forms.ModelChoiceField(
    #     widget=forms.HiddenInput,
    #     queryset=User.objects.all(),
    #     disabled=True,
    # )

    # parent_comment = forms.ModelChoiceField(
    #     widget=forms.HiddenInput,
    #     queryset=Comment.active_comments.all(),
    #     disabled=True,
    #     required=False,
    #     help_text='Select the parent if any',
    # )

    class Meta:
        model = Comment
        fields = ['post', 'body', 'parent_comment']


class PostForm(forms.ModelForm):
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        )

    class Meta:
        model = Post
        fields = ['title', 'body', 'topic', 'post_image']
