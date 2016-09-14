import json
from io import BytesIO

from django.http import FileResponse
from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response

import extractor.pdf
from book.models import Book
from book.serializers import BookSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def toc(self, request, pk):
        book = self.get_object()
        return Response(json.loads(book.toc_json))

    def read(self, request, pk, from_=None, to=None):
        book = self.get_object()

        if from_ is None and to is None:
            page_from = 1
            page_to = book.number_of_pages
        else:
            page_from = int(from_) if from_ else 1
            page_to = int(to) if to else page_from

        if not book.page_numbers_in_range(page_from, page_to):
            raise Http404

        if page_from == 1 and page_to == book.number_of_pages:
            stream = open(book.pdf_path, 'rb')
        else:
            data = extractor.pdf.get_pages(book.pdf_path, page_from, page_to)
            stream = BytesIO(data)
        response = FileResponse(stream, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename={title} (pg. {from_}-{to}).pdf'.format(
            title=book.title,
            from_=page_from,
            to=page_to)
        return response
