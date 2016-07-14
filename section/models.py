from django.db import models

from book.models import Book


# Create your models here.
class Section(models.Model):
    book = models.ForeignKey(Book)
    title = models.TextField()
    slugified = models.TextField()
    has_children = models.BooleanField()
    word_cloud_base64 = models.TextField(null=True)

    def __str__(self):
        return self.book.title + ' - ' + self.title


class Adjacency(models.Model):
    parent = models.ForeignKey(Section, related_name='parent')
    child = models.ForeignKey(Section, related_name='child')

    def get_book(self):
        return self.parent.book

    class Meta:
        unique_together = ('parent', 'child')
