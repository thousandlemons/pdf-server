from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from section.models import Section, Adjacency
from section.serializers import SectionSerializer
from section.services import get_children


class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (permissions.AllowAny,)

    def children(self, request, pk):
        section = self.get_object()
        children = get_children(section)
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data)
