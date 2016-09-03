from django.db import models

from section.models import Section
from version.models import Version


class Content(models.Model):
    section = models.ForeignKey(Section)
    version = models.ForeignKey(Version)
    text = models.TextField()

    def __str__(self):
        return '{section_title} @ ["{version_name}"]'.format(section_title=self.section.title, version_name=self.version.name)  # string.format() always preferred

    class Meta(object):
        unique_together = ('section', 'version')  # added unique together
