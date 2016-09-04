from rest_framework import serializers

from version.models import *


class VersionSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()
        return instance

    class Meta:
        model = Version
        fields = '__all__'
