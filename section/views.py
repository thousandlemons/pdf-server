from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from section.models import *
from section.serializers import *


class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (permissions.AllowAny,)

    def children(self, request, pk):
        section = self.get_object()
        adjacencies = Adjacency.objects.filter(parent=section)
        children = list()
        for adjacency in adjacencies:
            children.append(adjacency.child)
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data)
