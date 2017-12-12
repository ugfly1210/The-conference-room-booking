from django.contrib import admin

# Register your models here.

from app01 import models
admin.site.register(models.UserInfo)
admin.site.register(models.Book)
admin.site.register(models.MeetingRoom)
