from rest_framework import serializers

from section.models import Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'title', 'page', 'has_children', 'book', 'parent', 'previous', 'next')


class SectionInTocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'title', 'page')
