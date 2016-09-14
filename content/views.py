from django.http import Http404
from django.http import HttpResponse
from rest_framework import parsers
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from content.models import Content
from content.serializers import ContentSerializer
from section.models import Section
from version.models import Version


def _convert_to_int(*args):
    return (int(arg) if arg is not None else None for arg in args)


class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.version.owner == request.user


class PlainTextParser(parsers.BaseParser):
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()


class ContentViewSet(viewsets.GenericViewSet):
    serializer_class = ContentSerializer
    permission_classes = (permissions.IsAuthenticated, IsCreatorOrReadOnly,)
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
        text = ContentViewSet._get_content_or_404(section_pk, version_pk).text.strip()
        descendants = '\n'.join(
            ContentViewSet._recursive_aggregate(child.id, version_pk) for child in
            Section.objects.get(id=section_pk).get_children()).strip()

        if not text:
            return descendants
        elif not descendants:
            return text
        else:
            return '\n'.join([text, descendants])

    def aggregate(self, request, section_pk, version_pk=None):
        section_pk, version_pk = _convert_to_int(section_pk, version_pk)
        text = ContentViewSet._recursive_aggregate(section_pk, version_pk)
        return HttpResponse(text)

    def post(self, request, section_pk, version_pk=None):
        section_pk, version_pk = _convert_to_int(section_pk, version_pk)
        content = ContentViewSet._get_content_or_create(section_pk, version_pk)
        self.check_object_permissions(request, content)
        content.text = self.request.body.strip()
        content.save()
        return Response()
