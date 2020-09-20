from django.db import models
from tinymce import HTMLField
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager


class Category(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Post(models.Model):

    OPTIONS = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    overview = models.TextField(null=True)
    thumbnail = models.FileField(upload_to='blog/posts/%Y/%m/%d')
    image_caption = models.CharField(max_length=100, default='Photo by Blog')
    content = HTMLField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    tags = TaggableManager()
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    thumbsup = models.IntegerField(default='0')
    thumbsdown = models.IntegerField(default='0')
    thumbs = models.ManyToManyField(User, related_name='thumbs', default=None, blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    status = models.CharField(max_length=10, choices=OPTIONS, default='draft')
    publish_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def full_name(self):
        return self.author.first_name + ' ' + self.author.last_name

    def thumbnail_tag(self):
        if self.thumbnail.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.thumbnail.url))
        else:
            return ""

    def get_absolute_url(self):
        return reverse('blog_details', kwargs={'id': self.id, 'slug': self.slug})


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='blog/images/%Y/%m/%d')

    class Meta:
        verbose_name_plural = "Images"

    def __str__(self):
        return self.title


class Vote(models.Model):
    post = models.ForeignKey(Post, related_name='postid', on_delete=models.CASCADE, default=None, blank=True)
    user = models.ForeignKey(User, related_name='userid', on_delete=models.CASCADE, default=None, blank=True)
    vote = models.BooleanField(default=True)
