# Generated by Django 2.0.6 on 2018-07-04 09:52

from django.conf import settings
from django.db import migrations, models
import forum.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0002_auto_20180701_1651'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='topic',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='total_likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comment',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='liked_comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(upload_to=forum.models.Post.get_upload_path, verbose_name='文章图片'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=forum.models.UserProfile.get_upload_path),
        ),
    ]