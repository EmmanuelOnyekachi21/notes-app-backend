from django.shortcuts import get_object_or_404, render
"""
notes.views
====================

This module provides API views for managing Note objects in\
    the notes application.
It includes endpoints for listing, creating, retrieving, updating, and\
    deleting notes.
The views utilize Django REST Framework for serialization and request handling.
"""

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from notes.models import Note
from notes.serializers import NoteSerializer, NoteWriteSerializer


@api_view(['GET'])
def categorys(request):
    """
    List all available note categories.
    """
    categories = [
        {
            "value": category[0],
            "label": category[1]
        }
        for category in Note.CATEGORY_CHOICES
    ]
    return Response(categories, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def note_list(request):
    """
    List all notes or create a new note.

    GET:
        Returns a list of all notes.

    POST:
        Creates a new note with the provided data.
        Returns the created note data on success, or\
            validation errors on failure.
    """

    if request.method == 'GET':
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = NoteWriteSerializer(data=request.data)
        if serializer.is_valid():
            note = serializer.save()
            note_serializer = NoteSerializer(note)
            return Response(
                note_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def note_detail(request, slug):
    """
    Retrieve, update, partially update, or delete a specific note by slug.

    GET:
        Returns the details of the specified note.

    PUT:
        Updates the entire note with the provided data.

    PATCH:
        Partially updates the note with the provided data.

    DELETE:
        Deletes the specified note.
    """
    note = get_object_or_404(Note, slug=slug)

    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = NoteWriteSerializer(note, data=request.data)
        if serializer.is_valid():
            updated_note = serializer.save()
            update_serializer = NoteSerializer(updated_note)
            return Response(update_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = NoteWriteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            updated_note = serializer.save()
            update_serializer = NoteSerializer(updated_note)
            return Response(update_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        title = note.title
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
