from django.contrib import admin
from .models import ProgressPost, Comment


@admin.register(ProgressPost)
class ProgressPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'total_likes')
    list_filter = ('created_at',)
    search_fields = ('title', 'caption', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

    def total_likes(self, obj):
        return obj.total_likes()
    total_likes.short_description = 'Likes'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'post__title')


