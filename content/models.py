from django.db import models

from section.models import Section
from version.models import Version


class Content(models.Model):
    section = models.ForeignKey(Section)
    version = models.ForeignKey(Version)
    text = models.TextField()

    def __str__(self):
        return '{section} @ ["{version}"] by "{owner}"'.format(section=self.section.title,
                                                               version=self.version.name,
                                                               owner=self.version.owner)

    class Meta(object):
        unique_together = ('section', 'version')  # added unique together

    def is_owned_by(self, user):
        return self.version.is_owned_by(user)
