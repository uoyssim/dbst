from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Log(models.Model):
    dev = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return self.dev

class Dev(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    info = models.CharField(max_length=50)
    addr = models.TextField()
    setting = models.IntegerField()
    last_log = models.DateTimeField()
    mail_sent = models.IntegerField()
    def __str__(self):
        return self.info
