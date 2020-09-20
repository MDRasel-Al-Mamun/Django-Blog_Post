from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save


def user_directory_path(instance, filename):
    return 'user/avatars/{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    birthday = models.DateField(auto_now=False, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(blank=True, max_length=20)
    image = models.FileField(upload_to=user_directory_path, default='user/user.png')
    website_url = models.URLField(blank=True, default='https://mywebsite.com/')
    facebook_url = models.URLField(blank=True, default='https://www.facebook.com/')
    twitter_url = models.URLField(blank=True, default='https://twitter.com/')
    instagram_url = models.URLField(blank=True, default='https://www.instagram.com/')
    github_url = models.URLField(blank=True, default='https://github.com/')

    def __str__(self):
        return self.user.username

    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
