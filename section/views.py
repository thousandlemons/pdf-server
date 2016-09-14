import json

from rest_framework import viewsets
from rest_framework.response import Response

from section import services

from content.models import Content
from section.models import Section
from section.serializers import SectionSerializer
from version.serializers import VersionSerializer


class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def children(self, request, pk):
        section = self.get_object()
        children = section.get_children()
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data)

    def versions(self, request, pk):
        section = self.get_object()
        contents = Content.objects.filter(section=section)
        version_serializer = VersionSerializer([content.version for content in contents], many=True)
        return Response(version_serializer.data)

    def partial_toc(self, request, pk):
        section = self.get_object()
        toc_dict = json.loads(section.book.toc_json)
        result = services.recursive_search(toc_dict, section.id)
        return Response(result)
