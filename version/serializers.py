from rest_framework import serializers

from version.models import *


class VersionSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        return instance

    class Meta:
        model = Version
        fields = '__all__'
