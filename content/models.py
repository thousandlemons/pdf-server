from django.db import models

from section.models import Section
from version.models import Version


class Content(models.Model):
    section = models.ForeignKey(Section)
    version = models.ForeignKey(Version)
    text = models.TextField()

    def __str__(self):
        return "%s @ Version [%s]".format(self.section.title, self.version.name)  # string.format() always preferred

    class Meta(object):
        unique_together = ('section', 'version')  # added unique together
