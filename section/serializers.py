from rest_framework import serializers

from section.models import Section


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ('id', 'title', 'has_children')
