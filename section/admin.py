from django.contrib import admin
from pdf_server.admin import SuperuserOnlyAdmin

from section.models import *


@admin.register(Section)
class SectionAdmin(SuperuserOnlyAdmin):
    model_class = Section

    list_display = ('id', 'title', 'book', 'has_children')
    readonly_fields = ('book', 'has_children')
    search_fields = ('book', 'title')
    list_filter = ('book', )

    def has_add_permission(self, request):
        return False


@admin.register(Adjacency)
class AdjacencyAdmin(SuperuserOnlyAdmin):
    model_class = Adjacency

    list_display = ('id', 'get_book', 'parent', 'child')
    readonly_fields = ('parent', 'child')
    search_fields = ('parent', 'child')

    def has_add_permission(self, request):
        return False
