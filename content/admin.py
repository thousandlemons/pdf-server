from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import User

from book.models import Book
from content.models import Content
from pdf_server.admin import OwnerAndSuperuserOnlyAdmin


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


class OwnerListFilter(SimpleListFilter):
    title = 'owner'
    parameter_name = 'owner'

    def lookups(self, request, model_admin):
        users = set(User.objects.all())
        return [(user.id, user.username) for user in users]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(version__owner__id__exact=self.value())
        else:
            return queryset


@admin.register(Content)
class ContentAdmin(OwnerAndSuperuserOnlyAdmin):
    model_class = Content

    list_display = ('id', 'section', 'version')
    list_filter = (BookListFilter, OwnerListFilter, 'version',)

    search_fields = ('text',)
