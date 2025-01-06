from django.contrib import admin
from django.db.models import QuerySet
from .models import *

@admin.action(description="Activer les quizes séléctionnés")
def activate(modelAdmin, request, querySet: QuerySet):
    updated = querySet.update(is_active=True)
    modelAdmin.message_user(request, f"{updated} quiz(es) ont été activé(s).")

@admin.action(description="Désactiver les quizes séléctionnés")
def deactivate(modelAdmin, request, querySet: QuerySet):
    updated = querySet.update(is_active=False)
    modelAdmin.message_user(request, f"{updated} quiz(es) ont été désactivé(s).")

class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'is_active', 'created', 'updated')
    list_filter = ('author', 'is_active', 'created', 'updated')
    search_fields = ('title', 'author__username')
    ordering = ('-created',)
    fields = ('title', 'author', 'is_active')
    actions = [activate, deactivate]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(Choice)
