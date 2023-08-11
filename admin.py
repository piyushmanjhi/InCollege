from django.contrib import admin
from .models import Job, UserInfo, userSetting, Friend_Request
from .models import Notification, JobUserR

# Register your models here.
admin.site.register(Job)
admin.site.register(UserInfo)
admin.site.register(userSetting)
admin.site.register(Friend_Request)
admin.site.register(Notification)
admin.site.register(JobUserR)