from django.urls import path

from notes import views

urlpatterns = [
    path("notes/", views.note_list, name="notes"),
    path("notes/<slug:slug>/", views.note_detail, name="note-detail"),
    path('categories/', views.categorys, name='categorys'),
    path('create/', views.create_note, name='create-note'),
]
