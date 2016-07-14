# Create your views here.
import json

from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializers import BookSerializer


class BookList(APIView):
    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            book = Book.objects.get(id=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            raise Http404


class BookToc(APIView):
    def get(self, request, pk, format=None):
        try:
            book = Book.objects.get(id=pk)
            return Response(json.loads(book.toc_json))
        except Book.DoesNotExist:
            raise Http404
