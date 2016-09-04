from rest_framework import permissions
from rest_framework import viewsets

from version.serializers import *


class VersionPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        # any user can view
        if request.method in permissions.SAFE_METHODS:
            return True

        # only creators can update and delete
        if request.method in ('POST', 'DELETE'):
            return obj.created_by == request.user

        # authenticated users can create
        return request.user is not None


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = (VersionPermission,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
