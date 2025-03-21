from django.contrib import admin
from .models import Guestbook

class GuestbookAdmin(admin.ModelAdmin):
    list_display = ('author', 'created', 'active')
    list_filter = ('created', 'active')
    fields = ('author', 'content')