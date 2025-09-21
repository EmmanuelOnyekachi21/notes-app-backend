"""
notes.models
------------
This module defines the Note model for the notes application backend.
It provides the data structure and logic for storing and managing notes,
including categorization, slug generation, and timestamping.
"""
from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string


class Note(models.Model):
    """
    Represents a note in the notes application.

    Attributes:
        CATEGORY_CHOICES (tuple): Available categories for notes.
        title (CharField): The title of the note.
        body (TextField): The main content of the note.
        slug (SlugField): Unique slug for the note,\
            auto-generated from the title.
        category (CharField): The category of the note.
        created (DateTimeField): Timestamp when the note was created.
        updated (DateTimeField): Timestamp when the note was last updated.
    """
    CATEGORY_CHOICES = (
        ('BUSINESS', 'Business'),
        ('PERSONAL', 'Personal'),
        ('HEALTH', 'Health'),
        ('STUDY', 'Study'),
        ('WORK', 'Work'),
        ('IMPORTANT', 'Important')
    )
    category_colors = {
        "BUSINESS": "navy",
        "PERSONAL": "teal",
        "HEALTH": "green",
        "STUDY": "blue",
        "WORK": "orange",
        "IMPORTANT": "red",
    }
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='PERSONAL'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    @property
    def color(self):
        return self.category_colors[self.category]

    class Meta:
        """
        Meta:
        ordering (list): Orders notes by the 'updated' field.
        """
        ordering = ['-updated']

    def __str__(self):
        """
        Returns a string representation of the note.

        Returns:
            str: The title of the note.
        """
        return self.title

    def save(self, *args, **kwargs):
        """
        Saves the note instance to the database.

        If the slug is not set, generates a unique slug based on the title.
        Ensures slug uniqueness by appending a random string if necessary.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.slug:
            slug = slugify(self.title)
            base = slug
            while Note.objects.filter(slug=slug).exists():
                slug = f"{base}-{get_random_string(length=6)}"
            self.slug = slug
        super().save(*args, **kwargs)
