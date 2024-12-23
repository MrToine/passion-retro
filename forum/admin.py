from django.contrib import admin
from .models import Category, Forum, Topic, Post

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('name', 'description')
    ordering = ('-created',)
    fields = ('name', 'description')

class ForumAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'created', 'updated')
    list_filter = ('category', 'author', 'created', 'updated')
    search_fields = ('name', 'description')
    ordering = ('-created',)
    fields = ('category', 'author', 'name', 'description')

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created', 'updated')
    list_filter = ('forum', 'author', 'created', 'updated', 'state')
    search_fields = ('title',)
    ordering = ('-created',)
    fields = ('forum', 'author', 'title', 'state')

class PostAdmin(admin.ModelAdmin):
    list_display = ('type', 'topic', 'author', 'created', 'updated')
    list_filter = ('topic', 'author', 'created', 'updated', 'type')
    fields = ('topic', 'author', 'content', 'type')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
