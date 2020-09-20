from django.contrib import admin
from django.conf import settings
from filebrowser.sites import site
from django.urls import path, include
from django.conf.urls.static import static
from django.urls import path, re_path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^admin/filebrowser/', site.urls),
    re_path(r'^tinymce/', include('tinymce.urls')),

    path('', include('home.urls')),
    path('user/', include('user.urls')),
    path('blog/', include('blog.urls')),
    path('authentication/', include('authentication.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
