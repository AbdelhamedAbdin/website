from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify

CHOICE = [('male', 'male'), ('female', 'female')]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    overview = models.TextField(editable=True, blank=True, default='You have no an Overview yet')
    city = models.CharField(max_length=20, blank=False, default="USA")
    phone = models.IntegerField(default=0, blank=True)
    sex = models.CharField(max_length=10, default='male', choices=CHOICE)
    skill = models.CharField(max_length=100, default='You have no skills yet')
    logo = models.ImageField(upload_to='images/', default='images/default-logo.jpg', blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super().save(*args, **kwargs)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(receiver=create_profile, sender=User)
