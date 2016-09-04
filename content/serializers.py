from rest_framework import serializers

from content.models import *


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('text', )
