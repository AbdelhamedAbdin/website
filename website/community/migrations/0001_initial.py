# Generated by Django 3.0.7 on 2020-08-09 04:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAsking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Be specific and imagine you’re asking a question to another person', max_length=100)),
                ('clone_title', models.CharField(default='title', max_length=100)),
                ('question', models.TextField(help_text='Include all the information someone would need to answer your question', max_length=500)),
                ('field', models.CharField(choices=[('Technology', 'Technology'), ('Computer Science', 'Computer Science'), ('Lawyer', 'Lawyer'), ('Trading', 'Trading'), ('Engineering', 'Engineering'), ('Life Dialy', 'Life Dialy')], default='Technology', help_text='Add the field to describe what your question is about', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('ask_slug', models.SlugField(max_length=100)),
                ('dislikes', models.ManyToManyField(blank=True, related_name='dislikes', to=settings.AUTH_USER_MODEL)),
                ('favorite', models.ManyToManyField(blank=True, related_name='favorite', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('userprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(error_messages={'error': 'You have to write any word here'}, max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default='empty', max_length=30)),
                ('logo', models.ImageField(blank=True, default='images/default-logo.jpg', upload_to='images/')),
                ('username', models.CharField(default='empty', max_length=30)),
                ('comment_slug', models.SlugField(default='blank', max_length=100)),
                ('likes', models.ManyToManyField(blank=True, related_name='like_comment', to=settings.AUTH_USER_MODEL)),
                ('userasking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.UserAsking')),
                ('userprofile', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfile')),
            ],
        ),
    ]
