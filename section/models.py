from django.db import models

from book.models import Book


class Section(models.Model):
    book = models.ForeignKey(Book)
    title = models.TextField()
    page = models.IntegerField()
    has_children = models.BooleanField()

    parent = models.ForeignKey('Section', related_name='parent_section', null=True)
    previous = models.ForeignKey('Section', related_name='previous_section', null=True)
    next = models.ForeignKey('Section', related_name='next_section', null=True)

    def __str__(self):
        return "[{id}] {title}".format(id=self.id, title=self.title)

    def get_children(self):
        return Section.objects.filter(parent=self)
