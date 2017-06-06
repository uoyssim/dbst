# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_actor_director_group_group_auth_movie_posting'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('movie_id', models.IntegerField()),
                ('comment', models.TextField()),
                ('timestamp', models.DateTimeField()),
                ('like', models.IntegerField()),
                ('unlike', models.IntegerField()),
            ],
            options={
                'db_table': 'blog_comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Direct',
            fields=[
                ('direct_id', models.AutoField(primary_key=True, serialize=False)),
                ('movie_id', models.IntegerField()),
            ],
            options={
                'db_table': 'blog_direct',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.SmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre_id', models.AutoField(primary_key=True, serialize=False)),
                ('movie_id', models.IntegerField()),
                ('genre', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'blog_genre',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Posting_comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('comment', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'blog_posting_comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QA',
            fields=[
                ('qa_id', models.AutoField(db_column='QA_id', primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField()),
                ('category', models.CharField(max_length=50)),
                ('qa_title', models.CharField(blank=True, db_column='QA_title', max_length=50, null=True)),
                ('qa_contents', models.TextField(db_column='QA_contents')),
                ('state', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'blog_qa',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.AutoField(db_column='role_id', primary_key=True, serialize=False)),
                ('role', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'blog_role',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('score', models.IntegerField()),
            ],
            options={
                'db_table': 'blog_score',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Trailer',
            fields=[
                ('trailer_id', models.AutoField(primary_key=True, serialize=False)),
                ('trailer_name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'blog_trailer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=15)),
                ('reg_date', models.DateTimeField()),
                ('birthday', models.DateField()),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'user_info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'blog_user_interest',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='actor',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='dev',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='director',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='group_auth',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='log',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='posting',
            options={'managed': False},
        ),
    ]