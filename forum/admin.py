from django.contrib import admin
from .models import Category, Forum, Topic, Post

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('name', 'description')
    ordering = ('-created',)
    fields = ('name', 'description')

class ForumAdmin(admin.ModelAdmin):
    list_display = ('category', 'author', 'name', 'description', 'created', 'updated')
    list_filter = ('category', 'author', 'created', 'updated')
    search_fields = ('name', 'description')
    ordering = ('-created',)
    fields = ('category', 'author', 'name', 'description')

class TopicAdmin(admin.ModelAdmin):
    list_display = ('forum', 'author', 'title', 'created', 'updated', 'state')
    list_filter = ('forum', 'author', 'created', 'updated', 'state')
    search_fields = ('title',)
    ordering = ('-created',)
    fields = ('forum', 'author', 'title', 'state')

admin.site.register(Category)
admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Post)
