from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at',)

    list_filter = ('created_at', 'author',)

    search_fields = ('title', 'content', 'author__email',)

    readonly_fields = ('created_at',)
