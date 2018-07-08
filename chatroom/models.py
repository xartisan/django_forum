from django.db import models

from account.models import UserProfile
from common.model import BaseModel


class Group(BaseModel):
    name = models.CharField("群名", max_length=127)
    brief = models.CharField("群简介", max_length=255, default="")
    owner = models.ForeignKey(
        UserProfile,
        related_name="owned_groups",
        verbose_name="群主",
        on_delete=models.CASCADE)
    admins = models.ManyToManyField(
        UserProfile, blank=True, related_name="managed_groups", verbose_name="管理员")
    members = models.ManyToManyField(
        UserProfile, blank=True, related_name="belonged_groups", verbose_name="群成员")
    max_members_limit = models.PositiveIntegerField("最大成员数", default=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "群组"
        verbose_name_plural = verbose_name


class Message(BaseModel):
    MESSAGE_TYPE_CHOICES = (
        ('single', '个人'),
        ('group', '群'),
    )
    content = models.TextField()
    receiver = models.ForeignKey(
        to=UserProfile,
        related_name='msg_received',
        verbose_name='接收者',
        on_delete=models.CASCADE)
    sender = models.ForeignKey(
        to=UserProfile,
        related_name='msg_sent',
        verbose_name='发送者',
        on_delete=models.CASCADE)
    type = models.CharField(
        max_length=10,
        choices=MESSAGE_TYPE_CHOICES,
        default='single',
        verbose_name='信息类型(个人/群)')
