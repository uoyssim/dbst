# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    nation = models.CharField(max_length=50)
    count = models.IntegerField()
    score = models.IntegerField()
    picture_url = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'blog_actor'


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    movie_id = models.IntegerField()
    user = models.ForeignKey('User', models.DO_NOTHING)
    comment = models.TextField()
    timestamp = models.DateTimeField()
    like = models.IntegerField()
    unlike = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'blog_comment'

class Dev(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    info = models.CharField(max_length=50)
    addr = models.TextField()
    setting = models.IntegerField()
    last_log = models.DateTimeField()
    mail_sent = models.IntegerField()
    def __str__(self):
        return self.info
    class Meta:
        managed = False
        db_table = 'blog_dev'
        
class Direct(models.Model):
    direct_id = models.AutoField(primary_key=True)
    movie_id = models.IntegerField()
    director = models.ForeignKey('Director', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'blog_direct'


class Director(models.Model):
    director_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    birthday = models.DateField()
    nation = models.CharField(max_length=50)
    count = models.IntegerField()
    picture_url = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'blog_director'


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    movie_id = models.IntegerField()
    genre = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'blog_genre'


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=50)
    group_info = models.TextField()
    like = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'blog_group'


class Group_auth(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, primary_key=True)
    group = models.ForeignKey(Group, models.DO_NOTHING)
    auth = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blog_group_auth'
        unique_together = (('user', 'group'),)


class Log(models.Model):
    dev = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blog_log'


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title_kor = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100)
    playdate = models.DateField()
    playtime = models.CharField(max_length=4)
    year = models.CharField(max_length=4)
    nation = models.CharField(max_length=50)
    poster_url = models.CharField(max_length=200)
    class Meta:
        managed = False
        db_table = 'blog_movie'


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField()
    published_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'blog_post'


class Posting(models.Model):
    posting_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(Group, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=50)
    date = models.DateTimeField()
    contents = models.TextField(blank=True, null=True)
    count = models.IntegerField()
    like = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'blog_posting'


class Posting_comment(models.Model):
    posting = models.ForeignKey(Posting, models.DO_NOTHING)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blog_posting_comment'
        unique_together = (('posting', 'timestamp', 'user'),)


class QA(models.Model):
    qa_id = models.AutoField(db_column='QA_id', primary_key=True)  # Field name made lowercase.
    timestamp = models.DateTimeField()
    category = models.CharField(max_length=50)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    qa_title = models.CharField(db_column='QA_title', max_length=50, blank=True, null=True)  # Field name made lowercase.
    qa_contents = models.TextField(db_column='QA_contents')  # Field name made lowercase.
    state = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'blog_qa'


class Role(models.Model):
    role_id = models.AutoField(db_column='role_id', primary_key=True)
    movie = models.ForeignKey(Movie, models.DO_NOTHING, blank=True, null=True)
    actor = models.ForeignKey(Actor, models.DO_NOTHING, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blog_role'


class Score(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'blog_score'
        unique_together = (('user_id', 'movie'),)


class Trailer(models.Model):
    trailer_id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, models.DO_NOTHING, blank=True, null=True)
    trailer_name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'blog_trailer'


class UserInterest(models.Model):
    movie = models.ForeignKey(Movie, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blog_user_interest'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=15)
    reg_date = models.DateTimeField()
    birthday = models.DateField()
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'user'
