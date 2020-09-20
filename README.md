# Django User Blog Project

To Create a Full Blog for Django Website

> - <a href="#tinymce">1. Install TinyMCE Editor </a>

> - <a href="#model">2. Create Post Model With Multi Image & Taggit </a>

> - <a href="#home_blog">3. Show Posts In Home Page </a>

> - <a href="#post">4. Show All Blog Posts With Pagination  </a>

> - <a href="#ct_posts">5. Show Category & Tags Posts  </a>

> - <a href="#details">6. Blog Post Details With Multi Image Carousel </a>

> - <a href="#details">7. Sidebar With Django Custom Template Tags </a>

> - <a href="#feature">8. Blog Post Add Like & Bookmark Feature </a>

> - <a href="#search">9. Search Posts With AJAX Dropdowm Suggestion  </a>


## 1. Install TinyMCE Editor <a href="" name="tinymce"> - </a>

1. TinyMCE install - `pip install django-filebrowser-no-grappelli django-tinymce4-lite jsmin Pillow pytz`

* blogProject > settings > base.py 

```python
INSTALLED_APPS = [
    'filebrowser',   # Add top of the INSTALLED APPS
    'django.contrib.admin',

    'tinymce',
]

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 970,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins':
    '''
            textcolor save link image imagetools media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1':
    '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2':
    '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

```

* blogProject > urls.py

```python
from filebrowser.sites import site
from django.urls import path, re_path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^admin/filebrowser/', site.urls),
    re_path(r'^tinymce/', include('tinymce.urls')),
]

```

1. Add CSS & JS file - static > css/js - `github.css & highlight.pack.js`
2. Link to HTML filr - templates > base > css.html/js.html -

    `<link rel="stylesheet" href="{% static 'css/github.css' %}">`

    `<script type="text/javascript" src="{% static 'js/highlight.pack.js' %}"></script>`

3. Collect Static Files - `python manage.py collectstatic`


## 2. Create Post Model With Multi Image & Taggit <a href="" name="model"> - </a>

1. Create a blog app `python manage.py startapp blog`
2. Define install app - blogProject > settings > base.py - `'blog.apps.BlogConfig'`
3. Create url - blogProject > urls.py - `path('blog/', include('blog.urls')),`
4. Create url file - `blog > urls.py`
5. Install Taggit - `pip install django-taggit`


* blogProject > settings > base.py 

```python
INSTALLED_APPS = [
    'taggit',
]
```

* blog > models.py 

```python
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

```

* blog > admin.py 

```python
from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'date']
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)


class PostImageInline(admin.TabularInline):
    model = Images
    extra = 2


class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category', 'status', 'thumbnail_tag']
    list_filter = ['category']
    readonly_fields = ['thumbnail_tag']
    inlines = [PostImageInline]
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 10

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'image']
    search_fields = ['__str__']

    class Meta:
        model = Images


admin.site.register(Images, ImagesAdmin)

```
1. Run - `python manage.py makemigrations` & `python manage.py migrate`
2. Create some dummy post - `127.0.0.1:8000/admin`


## 3. Show Posts In Home Page <a href="" name="home_blog"> - </a>

* home > views.py 

```python
from django.shortcuts import render
from blog.models import Post


def homeView(request):
    posts = Post.objects.filter(status='Published').order_by('-id')
    context = {
        'posts': posts,
    }
    return render(request, 'home/index.html', context)
```

* templates > home > index.html

```html
{% if posts %}
{% for post in posts %}
<div class="col-sm-6 col-md-6 col-lg-4">
    <div class="card mb-4">
        <div class="img-box">
            <img class="card-img-top" src="{{ post.thumbnail.url }}" width="100%" height="250px" alt="Card image cap">
        </div>
        <div class="card-body">
            <span class="text text-warning text-uppercase">{{ post.category.name }}</span>
            <a class="text-decoration-none text-dark" href="{{ post.get_absolute_url }}">
                <h4 class="card-title text-capitalize">
                    {{ post.title|truncatewords:6 }}
                </h4>
            </a>
            <p class="card-text text-justify">{{ post.overview|truncatewords:12 }}</p>
            <a href="{{ post.get_absolute_url }}" class="btn btn-secondary">Read More &rarr;</a>
        </div>
        <div class="card-footer text-muted">
            <div class="">
                <span class="post-auhor-date">
                    <span>
                        <a href="" class="pr-1">
                            <img src="{{ post.author.userprofile.image.url }}" height="30px" width="30px" class="rounded-circle" alt="">
                        </a>
                    </span>
                    <span href="" class=""> {{ post.publish_date }}</span>
                </span>
                <span class="px-1"> | </span>
                <span class="post-readtime">
                    <i class="fal fa-clock"></i>1 min <span>read</span>
                </span>
            </div>
        </div>
    </div>
</div>
{% endfor %}
{% else %}
    <h4>There Are No Posts</h4>
{% endif %}
<div class="row mx-auto">
    <div class="col-md-12">
        <a href="{% url 'blog' %}" class="btn btn-outline-info align-center">Show All Posts &rarr;</a>
    </div>
</div>
```

## 4. Show All Blog Posts With Pagination <a href="" name="post"> - </a>

1. Create File > templates > blog - `blog.html`

* blog > views.py 

```python
from .models import Post
from django.shortcuts import render
from django.core.paginator import Paginator


# Blog Post Show 
def blogPosts(request):
    posts = Post.objects.filter(status='Published').order_by('-id')

    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    # Next Post
    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    # Previous Post
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

```

* blog > urls.py 

```python
from django.urls import path
from .import views

urlpatterns = [
    path('', views.blogPosts, name='blog'),
]

```

* templates > blog > blog.html

```html
<!-- Blog Post -->
{% if page %}
    {% for post in page.object_list %}
    <div class="card mb-4">
        <div class="img-box">
            <img class="card-img-top" src="{{ post.thumbnail.url }}" height="400" alt="Card image cap">
        </div>
        <div class="card-body">
            <span class="text text-warning text-uppercase">
                {{ post.category.name }}
            </span>
            <a class="text-decoration-none text-dark" href="{{ post.get_absolute_url }}">
                <h2 class="card-title text-capitalize">{{ post.title }}</h2>
            </a>
            <p class="card-text text-justify">{{ post.overview }}</p>
            <div class="mb-3">
                {% for tag in post.tags.all %}
                    <a href="{% url 'tagged' tag.slug %}" class="badge badge-primary">{{ tag }}</a>
                {% endfor %}
            </div>
            <a href="{{ post.get_absolute_url }}" class="btn btn-secondary">Read More &rarr;</a>
        </div>
        <div class="card-footer text-muted">
            <div class="">
                <span class="post-auhor-date">
                    <span>
                        <a href="" class="pr-1">
                            <img src="{{ post.author.userprofile.image.url }}" height="30px" width="30px" class="rounded-circle" alt="">
                        </a>
                    </span>
                    <span href="" class=""> {{ post.publish_date }} </span>
                </span>
                <span class="px-1"> | </span>
                <span class="post-readtime">
                    <i class="fal fa-clock"></i> 1 min <span>read</span>
                </span>
            </div>
        </div>
    </div>
    {% endfor %}
{% else %}
    <h3>No Posts are Published</h3>
{% endif %}


<!-- Pagination -->
<nav class="" aria-label="...">
    <ul class="pagination justify-content-center mb-4">
        <li class="page-item {% if not prev_page_url %} disabled {% endif %}">
            <a class="page-link" href="{{ prev_page_url }}" tabindex="-1">Previous</a>
        </li>
        {% for n in page.paginator.page_range %}
            {% if page.number == n %}
                <li class="page-item active">
                    <a class="page-link" href="?page={{ n }}">{{ n }}
                    <span class="sr-only">(current)</span>
                    </a>
                </li>
            {% elif n > page.number|add:-3 and n < page.number|add:3 %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ n }}">{{ n }}</a>
                </li>
            {% endif %}
        {% endfor %}
        <li class="page-item {% if not next_page_url %} disabled {% endif %}">
            <a class="page-link" href="{{ next_page_url }}">Next</a>
        </li>
    </ul>
</nav>
```

1. Add blog page link in navbaer - `<a href="{% url 'blog' %}" class="nav-item nav-link">Blog</a>`

## 5. Show Category & Tags Posts <a href="" name="ct_posts"> - </a>

1. Create File > templates > blog - `categoty.html` & `tags.html`

* blog > views.py 

```python
from taggit.models import Tag
from .models import Post, Images, Category
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404


# Tag Post Show
def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'blog/tags.html', context)

# Category Post Show
def category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=cat)
    context = {
        'cat': cat,
        'posts': posts,
    }
    return render(request, 'blog/categoty.html', context)

```

* blog > urls.py 

```python
from django.urls import path
from .import views

urlpatterns = [
    path('category/<slug:slug>/', views.category, name="category"),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
]

```

* templates > blog > tags.html & categoty.html

```html
<!-- Blog Post -->
{% if posts %}
    {% for post in posts %}
    <div class="card mb-4">
        <div class="img-box">
            <img class="card-img-top" src="{{ post.thumbnail.url }}" height="400" alt="Card image cap">
        </div>
        <div class="card-body">
            <span class="text text-warning text-uppercase">
                {{ post.category.name }}
            </span>
            <a class="text-decoration-none text-dark" href="{{ post.get_absolute_url }}">
                <h2 class="card-title text-capitalize">{{ post.title }}</h2>
            </a>
            <p class="card-text text-justify">{{ post.overview }}</p>
            <div class="mb-3">
                {% for tag in post.tags.all %}
                    <a href="{% url 'tagged' tag.slug %}" class="badge badge-primary">{{ tag }}</a>
                {% endfor %}
            </div>
            <a href="{{ post.get_absolute_url }}" class="btn btn-secondary">Read More &rarr;</a>
        </div>
        <div class="card-footer text-muted">
            <div class="">
                <span class="post-auhor-date">
                    <span>
                        <a href="" class="pr-1">
                            <img src="{{ post.author.userprofile.image.url }}" height="30px" width="30px" class="rounded-circle" alt="">
                        </a>
                    </span>
                    <span href="" class=""> {{ post.publish_date }} </span>
                </span>
                <span class="px-1"> | </span>
                <span class="post-readtime">
                    <i class="fal fa-clock"></i> 1 min <span>read</span>
                </span>
            </div>
        </div>
    </div>
    {% endfor %}
{% endif %}

```


## 6. Blog Post Details with Multi Image Carousel <a href="" name="details"> - </a>

1. Create File > templates > blog - `blog_details.html`

* blog > views.py 

```python
from django.db.models import Count
from .models import Post, Images, Category


def blogDetails(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    images = Images.objects.filter(post=post)
    context = {
        'post': post,
        'images': images,
    }
    return render(request, 'blog/blog_details.html', context)
```

* blog > urls.py

```py
urlpatterns = [
    path('<str:id>/<slug:slug>', views.blogDetails, name='blog_details'),
]
```

* templates > blog > blog.html

```html
<!-- Post Content Column -->
<div class="col-lg-8">

    <!-- Title -->
    <h1 class="mb-5">{{ post.title }}</h1>

    <!--Carousel Wrapper-->
    <div id="carousel-example-1z" class="carousel slide carousel-fade z-depth-1-half" data-ride="carousel">

        <!--Indicators-->
        <ol class="carousel-indicators">
            {% if images %}
                {% for pic in images %}
                    <li data-target="#carousel-example-1z" data-slide-to="{{ forloop.counter0 }}" class="{% if forloop.counter0 == 0 %} active {% endif %}"></li>
                {% endfor %}
            {% endif %}
        </ol>
        <!--/.Indicators-->

        <!--Sliders-->
        <div class="carousel-inner" role="listbox">

            <!-- slide-->
            {% if images %}
                {% for pic in images %}
                    <div class="carousel-item {% if forloop.counter0 == 0 %} active {% endif %}">
                        <img class="d-block w-100" src="{{ pic.image.url }}" alt="First slide">
                    </div>
                {% endfor %}
            {% else %}
                <img src="{{ post.thumbnail.url }}" class="img-fluid rounded" width="100%" height="500px" alt="">
            {% endif %}
            <!--slide-->
        </div>
        <!-- Sliders-->

        <!--Controls-->
        <a class="carousel-control-prev" href="#carousel-example-1z" role="button" data-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="sr-only">Previous</span>
        </a>
        <a class="carousel-control-next" href="#carousel-example-1z" role="button" data-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="sr-only">Next</span>
        </a>
        <!--/.Controls-->
    </div>
    <!--/.Carousel Wrapper-->

    <hr>
    <!-- Author -->
    <div class="">
        <span class="">
            <a href="" class="pr-1">
                <img src="{{ post.author.userprofile.image.url }}" height="30px" width="30px" class="rounded-circle" alt="">
            </a>
            <span>{{ post.full_name }}</span>
            <span class="px-1"> | </span>
            <span href="" class=""> {{ post.publish_date }} </span>
            <span class="px-1"> | </span>
            <span class="text-success text-uppercase">{{ post.category.name }}</span>
        </span>
        <span class="float-right">
            <span class="" id="like_count">1</span>
            <span class="px-2">
                <a class="" href="" value="">
                <i class="fad fa-heart fa-lg"></i>
                </a>
            </span>
            <span class="px-2">
                <a class="" href="">
                <i class="fal fa-bookmark fa-lg"></i>
                </a>
            </span>
        </span>
    </div>
    <hr>

    <!-- Post Content -->
    {{ post.content|safe }}

    <div class="mb-3">
        <h4>Tags In</h4>
        {% for tag in post.tags.all %}
            <a href="{% url 'tagged' tag.slug %}" class="badge badge-primary">{{ tag }}</a>
        {% endfor %}
    </div>

    <hr>
</div>
```

## 7. Sidebar With Django Custom Template Tags <a href="" name="sidebar"> - </a>

1. Create files - templatetags > `__init__.py` & `post_sidebar.py`
2. Create html file - templates > blog > `sidebar.html`

* blog > templatetags > post_sidebar.py 

```python
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

```

* templates > blog > sidebar.html

```html
{% load post_sidebar %}

<!-- Categories Widget -->
{% category_sidebar as categories %}
    {% for category in categories %}
        <li class="border-bottom py-1">
            <a class="text text-dark" href="{% url 'category' category.slug %}">{{ category.name }}
                <span class="float-right text-muted">({{ category.cat_num }})</span>
            </a>
        </li>
    {% endfor %}


<!-- Latest Post -->
{% latest_sidebar as latest_post%}
    {% for latest in latest_post %}
        <li class="border-bottom py-2">
            <div class="sidebar-thumb">
                <img class="rounded-circle" src="{{ latest.thumbnail.url }}" height="20px" width="20px" alt="" />
            </div>
            <div class="sidebar-content">
                <h5 class="">
                    <a href="{{ latest.get_absolute_url }}">{{ latest.title|truncatewords:6 }}</a>
                </h5>
            </div>
            <div class="sidebar-meta">
                <span class="time"><i class="fal fa-clock pr-1"></i>{{ latest.publish_date }}</span>
                <span class="comment"><i class="fa fa-comment"></i> 10 </span>
            </div>
        </li>
    {% endfor %}

<!-- tag -->
{% tag_sidebar as common_tags %}
    {% for common_tag in common_tags %}
        <div class="col-lg-4">
            <a href="{% url 'tagged' common_tag.slug %}" class="badge badge-info">{{ common_tag }}</a>
        </div>
    {% endfor %}
```

1. Include sidebar template on blog.html & blog_details.html - `{% include 'blog/sidebar.html' %}`


## 8. Blog Post Add Like & Bookmark Feature  <a href="" name="feature"> - </a>

1. Create file - templates > user > `bookmark.html`

* blog > models.py 

```python
class Post(models.Model):
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
```

1. Run - `python manage.py makemigrations` & `python manage.py migrate`


* user > views.py 

```python
from blog.models import Post
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='signin')
def favourite(request, id):
    post = get_object_or_404(Post, id=id)
    if post.favourites.filter(id=request.user.id).exists():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='signin')
def favourite_list(request):
    posts = Post.objects.filter(favourites=request.user)
    context = {
        'posts': posts,
    }
    return render(request, 'user/bookmark.html', context)


@csrf_exempt
@login_required(login_url='signin')
def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -= 1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count += 1
            result = post.like_count
            post.save()
        return JsonResponse({'result': result, })


```

* user > urls.py 

```python
urlpatterns = [
    path('favourite/<int:id>/', views.favourite, name='favourite'),
    path('profile/favourite/', views.favourite_list, name='favourite_list'),
    path('like/', views.like, name='like'),
]

```

* templates > user > bookmark.html

```html
{% if posts %}
    {% for post in posts %}
        <div class="col-sm-6 col-md-6 col-lg-4">
            <div class="card mb-4">
                <div class="img-box">
                    <img class="card-img-top" src="{{ post.thumbnail.url }}" width="100%" height="250px" alt="Card image cap">
                </div>
                <div class="card-body">
                    <span class="text text-warning text-uppercase">{{ post.category.name }}</span>
                    <a class="text-decoration-none text-dark" href="{{ post.get_absolute_url }}">
                        <h4 class="card-title text-capitalize">
                            {{ post.title|truncatewords:6 }}
                        </h4>
                    </a>
                    <p class="card-text text-justify">{{ post.overview|truncatewords:12 }}</p>
                </div>
                <div class="card-footer text-muted">
                    <div class="">
                    <span class="post-auhor-date">
                        <span>
                        <a href="" class="pr-1">
                            <img src="{{ post.author.userprofile.image.url }}" height="30px" width="30px"
                            class="rounded-circle" alt="">
                        </a>
                        </span>
                        <span href="" class=""> {{ post.publish_date }}</span>
                    </span>
                    <span class="px-1"> | </span>
                    <span class=""> &nbsp;
                        <a href="{% url 'favourite' post.id %}" data-type="add">
                            <i class="fad fa-bookmark"></i> <span class="text-muted">Remove</span>
                        </a>
                    </span>
                    </div>
                </div>
            </div>

        </div>
    {% endfor %}
{% else %}
    <h4 class="text-center">You are not select any favourite post</h4>
{% endif %}

```

* blog > views.py 

```py
def blogDetails(request, id, slug):
    favourite = bool
    if post.favourites.filter(id=request.user.id).exists():
        favourite = True
    context = {
        'favourite': favourite,
    }
    return render(request, 'blog/blog_details.html', context)
```

* templates > blog > blog_details.html

```html
<!-- Author & Feature -->
<span class="float-right">

    {% if request.user.is_authenticated %}
        <span class="text-warning" id="like_count">{{post.like_count}}</span>
        <span class="px-2">
            <button class="btn btn-link p-0 m-0 border-0 btn-outline-light" id="like-button" value="{{post.id}}">
                <i class="fad fa-heart fa-lg"></i>
            </button>
        </span>
        {% if favourite %}
            <span class="px-2">
                <a class="" href="{% url 'favourite' post.id %}">
                    <i class="fad fa-bookmark fa-lg"></i>
                    <span class="text-muted">Remove</span>
                </a>
            </span>
        {% else %}
            <span class="px-2">
                <a class="" href="{% url 'favourite' post.id %}">
                    <i class="fal fa-bookmark fa-lg"></i>
                </a>
            </span>
        {% endif %}

    {% else %}
        <span class="" id="like_count">{{post.like_count}}</span>
        <span class="px-2">
            <a class="" href="{% url 'signin' %}" value="{{post.id}}">
                <i class="fad fa-heart fa-lg"></i>
            </a>
        </span>
        <span class="px-2">
            <a class="" href="{% url 'signin' %}">
                <i class="fal fa-bookmark fa-lg"></i>
            </a>
        </span>
    {% endif %}
</span>

<!-- Add Javascript -->
<script>
  $(document).on('click', '#like-button', function (e) {
    e.preventDefault();
    $.ajax({
      type: 'POST',
      url: '{% url "like" %}',
      data: {
        postid: $('#like-button').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        action: 'post'
      },
      success: function (json) {
        document.getElementById("like_count").innerHTML = json['result']
      },
      error: function (xhr, errmsg, err) {

      }
    });
  })
</script>
```

1. Add Favourite Post Link - templates > partials > _header.html - `<a href="{% url 'favourite_list' %}" class="dropdown-item">Save Post</a>`


## 9. Search Posts With AJAX Dropdowm Suggestion  <a href="" name="search"> - </a>

1. Create File > templates > blog - `search.html`
2. Add CSS & javascript file - static > css/js - `jquery-ui.min.css` & `jquery-ui.min.js`
3. Link CSS & JS - templates > base > css/scripts - 

    `<link rel="stylesheet" href="{% static 'css/jquery-ui.min.css' %}">`

    `<script type="text/javascript" src="{% static 'js/jquery-ui.min.js' %}"></script>`

4. Create Form File > blog - `forms.py`

* blog > forms.py 

```py
from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=200)

```

* blog > views.py 

```py
import json
from .forms import SearchForm
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect


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

```

* blog > urls.py 

```py
urlpatterns = [
    path('search/', views.search, name='search'),
    path('search_auto/', views.searchAuto, name='search_auto'),
]

```

* templates > blog > sidebar.html

```html
<div class="card-body">
    <form action="/blog/search/" method="POST">
    <div class="input-group">
        {% csrf_token %}
        <input type="text" id="query" name="query" class="form-control" placeholder="Search for...">
        <span class="input-group-append">
        <button class="btn btn-secondary" type="submit">Go!</button>
        </span>
    </div>
    </form>
</div>
```

* templates > blog > search.html

```html
{% if posts %}
    {% for post in posts %}
        <div class="card mb-4">
            <div class="img-box">
                <img class="card-img-top" src="{{ post.thumbnail.url }}" height="400" alt="Card image cap">
            </div>
            <div class="card-body">
                <span class="text text-warning text-uppercase">
                    {{ post.category.name }}
                </span>
                <a class="text-decoration-none text-dark" href="{{ post.get_absolute_url }}">
                    <h2 class="card-title text-capitalize">{{ post.title }}</h2>
                </a>
                <p class="card-text text-justify">{{ post.overview }}</p>
                <div class="mb-3">
                    {% for tag in post.tags.all %}
                        <a href="{% url 'tagged' tag.slug %}" class="badge badge-primary">{{ tag }}</a>
                    {% endfor %}
                </div>
                    <a href="{{ post.get_absolute_url }}" class="btn btn-secondary">Read More &rarr;</a>
            </div>
            <div class="card-footer text-muted">
                <div class="">
                    <span class="post-auhor-date">
                        <span>
                            <a href="" class="pr-1">
                                <img src="{{ post.author.userprofile.image.url }}" height="30px" width="30px" class="rounded-circle" alt="">
                            </a>
                        </span>
                        <span href="" class=""> {{ post.publish_date }} </span>
                    </span>
                    <span class="px-1"> | </span>
                    <span class="post-readtime">
                        <i class="fal fa-clock"></i> 1 min <span>read</span>
                    </span>
                </div>
            </div>
        </div>
    {% endfor %}
{% else %}
    <h3>No Search Result Found</h3>
{% endif %}
```

* static > js > main.js

```js
// Search AutoComplete

$(function () {
  $('#query').autocomplete({
    source: '/blog/search_auto/',
    select: function (event, ui) {
      AutoCompleteSelectHandler(event, ui);
    },
    minLength: 2,
  });
});

function AutoCompleteSelectHandler(event, ui) {
  var selectedObj = ui.item;
}

```

## Run This Demo -

Steps:

1. Clone/pull/download this repository
2. Create a virtualenv with `virtualenv venv` and install dependencies with `pip install -r requirements.txt`
3. Configure your .env variables
4. Migrate all `python manage.py makemigrations` & `python manage.py migrate`
5. Create super user `python manage.py createsuperuser`
6. Collect all static files `python manage.py collectstatic`