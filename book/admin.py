from django.contrib import admin

from book.models import Book
from crawler.service import extract


def process_book(modeladmin, request, queryset):
    for book in queryset:
        if not book.is_processed:
            extract(book)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'is_processed')
    readonly_fields = ('is_processed', 'toc_json', 'root_section')
    search_fields = ('title',)
    ordering = ('title', )
    list_filter = ('is_processed', )
    actions = (process_book, )
