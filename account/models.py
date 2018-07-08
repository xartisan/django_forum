import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models

from common.model import BaseModel

User = get_user_model()


class UserProfile(BaseModel):

    def get_upload_path(self, filename):
        ext = os.path.splitext(filename)[1]
        return 'images/avatars/{}/{}{}'.format(self.id, uuid.uuid4(), ext)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=32)
    signature = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to=get_upload_path, blank=True, null=True)
    friends = models.ManyToManyField('self', related_name='my_friends', blank=True)

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
