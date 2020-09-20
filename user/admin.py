from django.contrib import admin
from user.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'designation', 'phone', 'image_tag']


admin.site.register(UserProfile, UserProfileAdmin)
