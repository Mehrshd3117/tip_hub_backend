from django.contrib import admin
from .models import Video, Subscriber, Like, IpAddress, VideoView, Category


class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "jalali_created", "category_to_str")
    list_filter = ("title", "created")
    search_fields = ("title", "description")

    def category_to_str(self, obj):
        return ", ".join([category.title for category in obj.category.all()])

    category_to_str.short_description = 'دسته بندی'


class VideoViewAdmin(admin.ModelAdmin):
    list_display = ("__str__", "created")
    list_filter = ("video", "created")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "parent")
    list_filter = ("slug", "title", "created", "updated")
    search_fields = ("title", "created", "slug", "updated")
    ordering = ['parent__id']


admin.site.register(Video, VideoAdmin)
admin.site.register(Subscriber)
admin.site.register(Like)
admin.site.register(IpAddress)
admin.site.register(Category, CategoryAdmin)
admin.site.register(VideoView, VideoViewAdmin)

