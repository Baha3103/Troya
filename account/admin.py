from django.contrib import admin

from .models import Post, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'body')


admin.site.register(Comment, CommentAdmin)