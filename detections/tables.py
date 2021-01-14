"""Model's tables."""

import django_tables2 as tables
from .models import Note

class NoteTable(tables.Table):
    class Meta:
        model = Note
        template_name = "django_tables2/bootstrap.html"
        fields = ('name', 'user', 'text', 'created')
