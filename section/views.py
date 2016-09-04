from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from content.models import Content
from section.models import Section
from section.serializers import SectionSerializer
from section.services import get_children
from version.serializers import VersionSerializer


class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (permissions.AllowAny,)

    def children(self, request, pk):
        section = self.get_object()
        children = get_children(section)
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data)

    def versions(self, request, pk):
        section = self.get_object()
        contents = Content.objects.filter(section=section)
        version_serializer = VersionSerializer([content.version for content in contents], many=True)
        return Response(version_serializer.data)
