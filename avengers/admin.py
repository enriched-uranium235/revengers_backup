from django.contrib import admin

from .models import Avengers, Message, Comment


admin.site.register(Avengers)
admin.site.register(Message)
admin.site.register(Comment)