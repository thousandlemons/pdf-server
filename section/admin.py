from django.contrib import admin

from section.models import *


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'book', 'has_children')
    search_fields = ('book', 'title')
    list_filter = ('book', 'has_children')


@admin.register(Adjacency)
class AdjacencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_book', 'parent', 'child')
    search_fields = ('parent', 'child')
