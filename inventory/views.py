from rest_framework import mixins, viewsets

from . serializers import BookSerializer
from . models import Book


class BookViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    @brief      Class for books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
