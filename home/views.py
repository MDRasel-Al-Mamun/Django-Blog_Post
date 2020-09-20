from django.shortcuts import render
from blog.models import Post, Category


def homeView(request):
    posts = Post.objects.filter(status='Published').order_by('-id')
    context = {
        'posts': posts,
    }
    return render(request, 'home/index.html', context)
