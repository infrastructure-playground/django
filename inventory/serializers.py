from rest_framework import serializers

from . models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    @brief      Class for author seriializer
    """
    class Meta:
        model = Book
        fields = '__all__'