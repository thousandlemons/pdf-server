from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.TextField()
    toc_html_path = models.TextField()
    target_dir_path = models.TextField(default='target/')
    is_processed = models.BooleanField(default=False)
    toc_json = models.TextField(null=True, blank=True)
    root_section = models.ForeignKey('section.Section', related_name='root_section', null=True, blank=True)

    def __str__(self):
        return self.title
