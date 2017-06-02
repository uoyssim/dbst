from django.contrib import admin
from .models import Post
from .models import Log

admin.site.register(Post)
admin.site.register(Log)
