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
