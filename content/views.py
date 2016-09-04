# Create your views here.
from django.http import Http404
from django.http import HttpResponse
from rest_framework import parsers
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from content.models import Content
from content.serializers import ContentSerializer
from section.services import get_children, Section
from version.models import Version


class ContentPermission(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        permitted_by_super = super().has_object_permission(request, view, obj)

        if request.method not in ('POST',):
            return permitted_by_super

        print(obj.version.created_by)
        print(request.user)

        return permitted_by_super and obj.version.created_by == request.user


def _convert_to_int(*args):
    return (int(arg) if arg is not None else None for arg in args)


class PlainTextParser(parsers.BaseParser):
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()


class ContentViewSet(viewsets.GenericViewSet):
    serializer_class = ContentSerializer
    permission_classes = (ContentPermission,)
    parser_classes = (PlainTextParser,)

    @staticmethod
    def _get_content_or_404(section_pk, version_pk):
        version_pk = version_pk if version_pk is not None else Version.objects.order_by('id')[0].id
        try:
            return Content.objects.get(section__id=section_pk, version__id=version_pk)
        except (Section.DoesNotExist, Version.DoesNotExist, Content.DoesNotExist):
            raise Http404

    @staticmethod
    def _get_content_or_create(section_pk, version_pk):
        try:
            section = Section.objects.get(id=section_pk)
            version = Version.objects.get(id=version_pk)
            return Content.objects.get(section=section, version=version)
        except (Section.DoesNotExist, Version.DoesNotExist):
            raise Http404
        except Content.DoesNotExist:
            return Content.objects.create(section=section, version=version, text='')

    def immediate(self, request, section_pk, version_pk=None):
        section_pk, version_pk = _convert_to_int(section_pk, version_pk)
        content = self._get_content_or_404(section_pk, version_pk)
        return HttpResponse(content.text)

    @staticmethod
    def _recursive_aggregate(section_pk, version_pk):
        content = ContentViewSet._get_content_or_404(section_pk, version_pk)
        return content.text + '\n' + '\n'.join(
            ContentViewSet._get_content_or_404(child.pk, version_pk).text for child in
            get_children(Section.objects.get(id=section_pk)))

    def aggregate(self, request, section_pk, version_pk=None):
        section_pk, version_pk = _convert_to_int(section_pk, version_pk)
        return HttpResponse(ContentViewSet._recursive_aggregate(section_pk, version_pk))

    def post(self, request, section_pk, version_pk=None):
        section_pk, version_pk = _convert_to_int(section_pk, version_pk)
        content = ContentViewSet._get_content_or_create(section_pk, version_pk)
        self.check_object_permissions(request, content)
        content.text = self.request.data
        content.save()
        return Response()
