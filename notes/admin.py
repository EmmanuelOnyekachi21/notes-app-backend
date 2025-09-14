"""
notes.admin
==============
This module configures the Django admin interface for the Note model.
It registers the Note model with custom display options for easier management.

    Admin configuration for the Note model.

    Displays the following fields in the admin list view:
        - title
        - slug
        - category
        - created
        - updated
"""
from django.contrib import admin

from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Note model, specifying fields\
        to display in the list view.
    """
    list_display = [
        'title', 'slug', 'category', 'created', 'updated'
    ]
