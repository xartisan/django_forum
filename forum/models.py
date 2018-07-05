import os
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Manager
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase

from common.model import BaseModel

User = get_user_model()


class PublishedManager(models.Manager):

    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset().filter(status='published')


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class Post(BaseModel):

    def get_upload_path(self, filename):
        ext = os.path.splitext(filename)[1]
        return 'images/posts/{}/{}.{}'.format(self.id, uuid.uuid4(), ext)

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    topic = models.ForeignKey(
        to='Topic', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField('标题', max_length=255)
    body = models.TextField('内容')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    publish = models.DateTimeField(default=timezone.now)
    post_image = models.ImageField('文章图片', upload_to=get_upload_path)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='posts_liked', blank=True)

    # managers
    objects = Manager()
    published = PublishedManager()
    tags = TaggableManager(through=UUIDTaggedItem)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:post_detail', args=[self.id])


class ActiveCommentManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Comment(BaseModel):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        to=Post,
        verbose_name='所属文章',
        on_delete=models.CASCADE,
        related_name='comments')
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='sub_comments',
        blank=True,
        null=True)
    body = models.TextField('评论内容')
    active = models.BooleanField(default=True)
    total_likes = models.PositiveIntegerField(default=0)
    users_like = models.ManyToManyField(
        to=User, related_name='liked_comment', blank=True)

    objects = Manager()
    active_comments = ActiveCommentManager()

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.post)


class MenuTopicManager(models.Manager):

    def get_queryset(self):
        return super(
            MenuTopicManager,
            self).get_queryset().filter(is_top_menu=True).order_by('position')


class Topic(BaseModel):
    name = models.CharField(max_length=32, unique=True)
    is_top_menu = models.BooleanField(default=False)
    position = models.SmallIntegerField()
    admins = models.ManyToManyField(User, blank=True)

    # managers
    objects = Manager()
    menu_topics = MenuTopicManager()

    class Meta:
        verbose_name = '主题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserProfile(BaseModel):

    def get_upload_path(self, filename):
        ext = os.path.splitext(filename)[1]
        return 'images/avatars/{}/{}{}'.format(self.id, uuid.uuid4(), ext)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=32)
    signature = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    user_from = models.ForeignKey(
        'auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(
        'auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


User.add_to_class('following',
                  models.ManyToManyField(
                      'self',
                      through=Contact,
                      related_name='followers',
                      symmetrical=False))
