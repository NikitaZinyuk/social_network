from django.contrib import admin
from .models import Post, Like


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = (LikeInline,)
    list_display = ('title', 'author', 'created_at')
    list_filter = ('created_at',)
