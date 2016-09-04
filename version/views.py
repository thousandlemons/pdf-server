from rest_framework import permissions
from rest_framework import viewsets

from version.serializers import *


class VersionPermission(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        permitted_by_super = super().has_object_permission(request, view, obj)

        if request.method not in ('POST', 'DELETE'):
            return permitted_by_super

        return permitted_by_super and obj.created_by == request.user


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = (VersionPermission,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
