from django.contrib import admin

from chatroom.models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    exclude = ()
