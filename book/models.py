from django.db import models


class Book(models.Model):
    title = models.TextField()
    toc_html_path = models.TextField()
    is_processed = models.BooleanField(default=False)
    toc_json = models.TextField(null=True, blank=True)
    root_section = models.ForeignKey('section.Section', related_name='root_section', null=True, blank=True)

    def __str__(self):
        return self.title
