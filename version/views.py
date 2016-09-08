from rest_framework import permissions
from rest_framework import viewsets

from version.serializers import *


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = (permissions.IsAuthenticated, IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
