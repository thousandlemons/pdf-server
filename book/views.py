import json

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from book.models import Book
from book.serializers import BookSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.AllowAny,)

    def toc(self, request, pk):
        book = self.get_object()
        return Response(json.loads(book.toc_json))
