"""
notes.serializers
~~~~~~~~~~~~~~~~~

Serializers for the notes app, providing translation between\
    Note model instances
and their JSON representations for API consumption.

Classes:
    NoteSerializer: Serializes Note model instances, including category display

"""
from rest_framework import serializers
from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Note model.

    Exposes both the raw category value and its human-readable label via
    `category_display`, which utilizes Django's `get_FOO_display()` method.
    This allows API consumers to use internal value for logic and filtering,
    while displaying a user-friendly label in the frontend.

    Fields:
        id (int): Unique identifier for the note.
        title (str): Title of the note.
        category (str): Raw category value (for internal logic/filtering).
        category_display (str): Human-readable category label (for UI display)
        slug (str): URL-friendly identifier for the note (read-only).
        created (datetime): Timestamp when the note was created (read-only).
        updated (datetime): Timestamp when the note was last updated\
            (read-only)
        body (str): Content of the note.
    """
    # category_display field uses get_category_display method from Note model.
    # 🔹 category_display uses Django’s built-in `get_FOO_display()` method.
    # Since `category` is a choices field, Django automatically creates:
    #   note.get_category_display() → returns the human-readable label.
    # Example:
    #   note.category = "BUSINESS"   (raw value stored in DB)
    #   note.get_category_display() → "Business" (label from choices tuple)
    #
    # We expose both in the API:
    #   - category = "BUSINESS" (for internal logic & filtering)
    #   - category_display = "Business" (for frontend UI display)
    category_display = serializers.CharField(
        source="get_category_display",
        read_only=True
    )

    class Meta:
        """
        Meta class for Note serializer.
        Attributes:
            model (Note): Specifies the model to be serialized.
            fields (list): List of fields to include in the serialized output.
            read_only_fields (list): Fields that are read-only and\
                cannot be modified through the serializer.
        """
        model = Note
        fields = [
            'id', 'title', 'category', 'category_display', 'slug', 'created',
            'updated', 'body'
        ]
        read_only_fields = [
            "slug", "created", "updated"
        ]


class NoteWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for writing Note objects.
    This serializer overrides the 'category' field to provide custom\
        validation
    and error messages for invalid category choices. It validates that the
    provided category is one of the allowed choices defined in the Note model's
    CATEGORY_CHOICES.
    Fields:
        title (str): The title of the note.
        category (str): The category of the note.\
            Must be one of the valid choices.
        body (str): The body/content of the note.
    Methods:
        validate_category(attrs): Validates that the category is\
            among the allowed choices.
            Raises:
                serializers.ValidationError: If the category is not valid.
    """
    # Override category field so we can control validation
    # Without overriding, DRF default error message pops
    category = serializers.CharField()

    class Meta:
        """
        Meta class for NoteWriteSerializer.
        Attributes:
            model (Note): specifies model to be serialized.
            fields (list): List of fields to be accepted as input from user.
        """
        model = Note
        fields = [
            'title', 'category', 'body'
        ]

    def validate_category(self, attrs):
        """
        Validates that the provided category is among the allowed choices\
            defined in Note.CATEGORY_CHOICES.
        Args:
            attrs (str): The category value to validate.
        Raises:
            serializers.ValidationError: If the category is not a valid\
                choice.
        Returns:
            str: The validated category value.
        """
        valid_choices = [
            choice[0] for choice in Note.CATEGORY_CHOICES
        ]
        if attrs not in valid_choices:
            raise serializers.ValidationError(
                f"Invalid Category '{attrs}'."
                f" Please choose from: {', '.join(valid_choices)}."
            )
        return attrs
