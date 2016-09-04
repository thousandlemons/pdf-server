# Create your views here.
import json

from django.http import Http404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from content.models import Content
from content.serializers import ContentSerializer


class ContentPermission(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        permitted_by_super = super().has_object_permission(request, view, obj)

        if request.method not in ('POST', ):
            return permitted_by_super

        return permitted_by_super and obj.version.created_by == request.user


class ContentViewSet(viewsets.GenericViewSet):
    queryset = Content.objects.all()
    permission_classes = (ContentPermission, )
