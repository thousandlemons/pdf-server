from rest_framework import serializers

from book.models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'pages', 'root_section')
