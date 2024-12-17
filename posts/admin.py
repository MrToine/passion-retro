from django.contrib import admin
from .models import Post, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'type', 'active', 'created', 'updated')
    list_filter = ('category', 'type', 'active', 'created', 'updated')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created',)
    fields = ('title', 'slug', 'category', 'content', 'type', 'image', 'author', 'active')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Category)