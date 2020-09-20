from django import template
from blog.models import *
from django.db.models import Count


register = template.Library()


@register.simple_tag
def latest_sidebar(count=4):
    return Post.objects.filter(status='Published').order_by('-id')[:count]


@register.simple_tag
def category_sidebar(count=5):
    return Category.objects.filter(status='True').order_by(
        '-id').annotate(cat_num=Count('post'))[:count]


@register.simple_tag
def tag_sidebar(count=9):
    return Post.tags.most_common()[:count]
