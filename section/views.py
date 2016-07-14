import base64

from django.http import Http404, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from section.models import *
from section.serializers import *
from section.services import get_content, get_content_aggregate


# Create your views here.

class SectionDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            section = Section.objects.get(id=pk)
            serializer = SectionSerializer(section)
            return Response(serializer.data)
        except Section.DoesNotExist:
            raise Http404


class ChildrenList(APIView):
    def get(self, request, pk, format=None):
        try:
            section = Section.objects.get(id=pk)
            adjacencies = Adjacency.objects.filter(parent=section)
            children = list()
            for adjacency in adjacencies:
                children.append(adjacency.child)
            serializer = SectionSerializer(children, many=True)
            return Response(serializer.data)
        except Section.DoesNotExist:
            raise Http404


class WordCloud(APIView):
    def get(self, request, pk, format=None):
        try:
            section = Section.objects.get(id=pk)
            return HttpResponse(base64.b64decode(section.word_cloud_base64), content_type='image/jpeg')
        except Section.DoesNotExist:
            raise Http404


class SectionContent(APIView):
    def get(self, request, pk, format=None):
        try:
            section = Section.objects.get(id=pk)
            return Response({'content': get_content(section)})
        except Section.DoesNotExist:
            raise Http404


class SectionContentAggregate(APIView):
    def get(self, request, pk, format=None):
        try:
            section = Section.objects.get(id=pk)
            return Response({'content': get_content_aggregate(section)})
        except Section.DoesNotExist:
            raise Http404
