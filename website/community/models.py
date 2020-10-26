from django.db import models
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
import datetime
from notifications.signals import notify
from django.db.models.signals import post_save
import notifications


CHOICE = [('Technology', 'Technology'), ('Computer Science', 'Computer Science'),
          ('Lawyer', 'Lawyer'), ('Trading', 'Trading'),
          ('Engineering', 'Engineering'), ('Life Dialy', 'Life Dialy')
]


class UserAsking(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, help_text='Be specific and imagine you’re asking a question to another person')
    clone_title = models.CharField(max_length=100, default='title')
    question = models.TextField(max_length=500, blank=False, help_text='Include all the information someone would need to answer your question')
    field = models.CharField(max_length=20, choices=CHOICE, default='Technology', help_text='Add the field to describe what your question is about')
    date = models.DateTimeField(auto_now_add=True)
    ask_slug = models.SlugField(max_length=100, allow_unicode=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    favorite = models.ManyToManyField(User, related_name='favorite', blank=True)

    def __str__(self):
        return self.clone_title

    def get_absolute_url(self):
        return reverse('community:question_view', kwargs={'user_slug': self.ask_slug})

    def arabic_slugify(self, str):
        str = str.replace(" ", "-")
        str = str.replace(",", "-")
        str = str.replace("(", "-")
        str = str.replace(")", "")
        str = str.replace("؟", "")
        return str

    # def save(self, *args, **kwargs):
    #     if not self.ask_slug:
    #         self.ask_slug = slugify(self.title)
    #         if not self.ask_slug:
    #             self.ask_slug = self.arabic_slugify(self.title)
    #     self.clone_title = '{}-{}'.format(self.ask_slug, id(self.ask_slug))
    #     if UserAsking.objects.filter(ask_slug=self.ask_slug).exists():
    #         self.ask_slug = self.clone_title
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.ask_slug = slugify(self.title)
        self.clone_title = '{}-{}'.format(self.ask_slug, id(self.ask_slug))
        if UserAsking.objects.filter(ask_slug=self.ask_slug).exists():
            self.ask_slug = self.clone_title
        super().save(*args, **kwargs)

    def get_unique_id(self):
        return id(self.pk)


class Comment(models.Model):
    userasking = models.ForeignKey(UserAsking, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, blank=False, error_messages={'error': 'You have to write any word here'})
    date = models.DateTimeField(auto_now_add=True)
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=30, blank=False, default='empty')
    logo = models.ImageField(upload_to='images/', default='images/default-logo.jpg', blank=True)
    username = models.CharField(max_length=30, blank=False, default='empty')
    comment_slug = models.SlugField(max_length=100, default='blank')
    likes = models.ManyToManyField(User, related_name='like_comment', blank=True)
    notify_comment = models.ManyToManyField(User, related_name='notify_comment_like', blank=True)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('community:question_view', kwargs={'user_slug': self.comment_slug})

    def slug(self):
        return self.comment_slug

    def get_id(self):
        return self.pk

    def save(self, *args, **kwargs):
        self.comment_slug = slugify(self.userasking.ask_slug)
        # self.userprofile.user
        notify.send(sender=self.userprofile.user,
                    recipient=self.userasking.userprofile.user,
                    action_object=self.userasking,
                    target=self,
                    verb="commented on")
        super().save(*args, **kwargs)
