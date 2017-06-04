from django.db import models
from django.utils import timezone
#Database
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

class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title_kor = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)
    playdate = models.DateField()
    playtime = models.CharField(max_length=4)
    year = models.CharField(max_length=4)
    nation = models.CharField(max_length=50)
    poster_url = models.CharField(max_length=200)

    def __str__(self):
        return self.title_kor


#WIRELESS
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

