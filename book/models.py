from django.db import models


class Book(models.Model):
    title = models.TextField()
    toc_html_path = models.TextField()
    pdf_path = models.TextField()
    pages = models.IntegerField(null=True)
    is_processed = models.BooleanField(default=False)
    root_section = models.ForeignKey('section.Section', related_name='root_section', null=True, blank=True)
    toc_json = models.TextField(null=True, blank=True)

    def __str__(self):
        return "[{id}] {title}".format(id=self.id, title=self.title)

    def root_section_id(self):
        return self.root_section.id

    def page_numbers_in_range(self, *args):
        for page_number in args:
            if not 1 <= page_number <= self.pages:
                return False
        return True
