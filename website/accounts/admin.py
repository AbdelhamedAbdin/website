from django.contrib import admin
from .models import *
from django.contrib.contenttypes.models import ContentType


admin.site.register(UserProfile)
admin.site.register(ContentType)
