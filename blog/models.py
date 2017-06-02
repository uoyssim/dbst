from django.db import models
from django.utils import timezone
import datetime

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
    def __str__(self):
        return self.info
		
class Actor(models.Model):
	actor_id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	#birthday = models.DateTimeField 왜 안되는지 이유좀
	nation = models.CharField(max_length=50)
	count = models.IntegerField()
	score = models.IntegerField()
	picture_url = models.CharField(max_length=100)
	def __str__(self):
		return self.name
	

class Movie(models.Model):
	movie_id = models.IntegerField()
	title_kor = models.CharField(max_length=100)
	title_en = models.CharField(max_length=100)
	playdate = models.DateTimeField()
	playtime = models.CharField(max_length=100)
	year = models.IntegerField()
	nation = models.CharField(max_length=50)
	poster_url = models.CharField(max_length=100)
	def __str__(self):
		return self.title_kor