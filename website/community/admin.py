from django.contrib import admin
from .models import UserAsking, Comment


admin.site.register(UserAsking)
admin.site.register(Comment)
# admin.site.register(Notification)