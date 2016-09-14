from django.contrib import admin

from pdf_server.admin import SuperuserOnlyAdmin
from section.models import *


@admin.register(Section)
class SectionAdmin(SuperuserOnlyAdmin):
    model_class = Section

    list_display = ('id', 'title', 'book', 'page', 'has_children')
    readonly_fields = ('book', 'page', 'has_children', 'parent', 'previous', 'next')
    search_fields = ('title', 'book')
    list_filter = ('book',)

    def has_add_permission(self, request):
        return False
