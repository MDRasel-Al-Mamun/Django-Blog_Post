import json
from taggit.models import Tag
from .forms import SearchForm
from django.db.models import Count
from django.http import HttpResponse
from .models import Post, Images, Category
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect



def blogPosts(request):
    posts = Post.objects.filter(status='Published').order_by('-id')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''
    context = {
        'page': page,
        'next_page_url': next_url,
        'prev_page_url': prev_url,
    }
    return render(request, 'blog/blog.html', context)


def blogDetails(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    images = Images.objects.filter(post=post)
    favourite = bool
    if post.favourites.filter(id=request.user.id).exists():
        favourite = True
    context = {
        'post': post,
        'images': images,
        'favourite': favourite,
    }
    return render(request, 'blog/blog_details.html', context)


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'blog/tags.html', context)


def category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=cat)
    context = {
        'cat': cat,
        'posts': posts,
    }
    return render(request, 'blog/categoty.html', context)


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            posts = Post.objects.filter(title__icontains=query)
            context = {
                'posts': posts,
                'query': query,
            }
            return render(request, 'blog/search.html', context)
    return HttpResponseRedirect('blog')


def searchAuto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        posts = Post.objects.filter(title__icontains=q)

        results = []
        for post in posts:
            post_json = {}
            post_json = post.title
            results.append(post_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
