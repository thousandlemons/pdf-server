from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from book.models import Book
from content.models import Content
from pdf_viewer_server.admin import ObjectLevelPermissionAdmin


class BookListFilter(SimpleListFilter):
    title = 'book'
    parameter_name = 'book'

    def lookups(self, request, model_admin):
        books = set(Book.objects.all())
        return [(book.id, book.title) for book in books]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(section__book__id__exact=self.value())
        else:
            return queryset


@admin.register(Content)
class ContentAdmin(ObjectLevelPermissionAdmin):
    model_class = Content

    list_display = ('id', 'section', 'version')
    list_filter = (BookListFilter, 'version',)

    search_fields = ('text',)
