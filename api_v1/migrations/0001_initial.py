# Generated by Django 4.0.6 on 2022-08-07 23:04

import api_v1.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='U_ID')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='username')),
                ('password', models.CharField(max_length=64, verbose_name='password')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('uid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api_v1.user', verbose_name='U_ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True, verbose_name='name')),
                ('avatar', models.ImageField(blank=True, max_length=256, null=True, upload_to=api_v1.models.avatar_dic_path, verbose_name='avatar')),
                ('gender', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], null=True, verbose_name='gender')),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='age')),
                ('email', models.EmailField(blank=True, max_length=256, null=True, verbose_name='email')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='phone_number')),
                ('join_time', models.DateField(auto_now_add=True, verbose_name='join_time')),
            ],
        ),
        migrations.CreateModel(
            name='UserFollowed',
            fields=[
                ('uid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='+', serialize=False, to='api_v1.user', verbose_name='U_ID')),
                ('followed_by', models.ManyToManyField(related_name='+', to='api_v1.user', verbose_name='followed_by')),
            ],
        ),
        migrations.CreateModel(
            name='UserFollow',
            fields=[
                ('uid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='+', serialize=False, to='api_v1.user', verbose_name='U_ID')),
                ('follow', models.ManyToManyField(related_name='+', to='api_v1.user', verbose_name='follow')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('rid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='R_ID')),
                ('title', models.CharField(max_length=64, verbose_name='title')),
                ('r_type', models.PositiveSmallIntegerField(choices=[(1, 'article'), (2, 'picture'), (3, 'video')], verbose_name='resource_type')),
                ('views_count', models.PositiveBigIntegerField(blank=True, default=0, null=True, verbose_name='numbers_of_views')),
                ('comments_count', models.PositiveBigIntegerField(blank=True, default=0, null=True, verbose_name='numbers_of_comments')),
                ('likes_count', models.PositiveBigIntegerField(blank=True, default=0, null=True, verbose_name='numbers_of_likes')),
                ('content', models.TextField(blank=True, null=True, verbose_name='content')),
                ('media', models.FileField(blank=True, max_length=256, null=True, upload_to=api_v1.models.avatar_dic_path, verbose_name='media')),
                ('release_time', models.DateTimeField(auto_now_add=True, verbose_name='release_time')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v1.userinfo', verbose_name='publisher')),
            ],
        ),
        migrations.CreateModel(
            name='PetInfo',
            fields=[
                ('pid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='P_ID')),
                ('pet_name', models.CharField(max_length=32, verbose_name='pet_name')),
                ('pet_avatar', models.ImageField(blank=True, max_length=256, null=True, upload_to=api_v1.models.avatar_dic_path, verbose_name='pet_avatar')),
                ('pet_gender', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], null=True, verbose_name='pet_gender')),
                ('pet_age', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='pet_age')),
                ('pet_type', models.CharField(blank=True, max_length=32, null=True, verbose_name='pet_type')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v1.userinfo', verbose_name='master_id')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('cid', models.BigAutoField(primary_key=True, serialize=False, verbose_name='C_ID')),
                ('content', models.TextField(verbose_name='content')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v1.resource', verbose_name='resource')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_v1.userinfo', verbose_name='publisher')),
            ],
        ),
        migrations.CreateModel(
            name='ResourceLike',
            fields=[
                ('uid', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='+', serialize=False, to='api_v1.userinfo', verbose_name='U_ID')),
                ('like', models.ManyToManyField(related_name='+', to='api_v1.resource', verbose_name='like_resource')),
            ],
        ),
    ]