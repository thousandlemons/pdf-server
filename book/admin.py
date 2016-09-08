from django.contrib import admin

from pdf_server.admin import SuperuserOnlyAdmin
from book.models import Book
from extractor import service


def process_book(modeladmin, request, queryset):
    for book in queryset:
        if not book.is_processed:
            service.extract(book)


@admin.register(Book)
class BookAdmin(SuperuserOnlyAdmin):
    model_class = Book

    exclude = ('root_section', )
    list_display = ('title', 'id', 'is_processed')
    readonly_fields = ('id', 'is_processed', 'root_section_id', 'toc_json')
    search_fields = ('title',)
    ordering = ('title',)
    list_filter = ('is_processed',)
    actions = (process_book,)

    superuser_only_fields = ('toc_html_path',)
    superuser_only_actions = (process_book, )

    # def get_list_display(self, request):
    #     return self.list_display + ('is_processed',) if self.is_superuser(request) else self.list_display
