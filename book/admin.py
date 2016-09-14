from django.contrib import admin

from book.models import Book
from extractor import service
from pdf_server.admin import SuperuserOnlyAdmin


def process_book(modeladmin, request, queryset):
    for book in queryset:
        if not book.is_processed:
            service.extract(book)


@admin.register(Book)
class BookAdmin(SuperuserOnlyAdmin):
    model_class = Book

    exclude = ('root_section',)
    list_display = ('title', 'id', 'is_processed')
    readonly_fields = ('id', 'number_of_pages', 'is_processed', 'root_section_id', 'toc_json')
    search_fields = ('title',)
    ordering = ('title',)
    list_filter = ('is_processed',)
    actions = (process_book,)

    superuser_only_fields = ('toc_html_path', 'pdf_path')
    superuser_only_actions = (process_book,)
