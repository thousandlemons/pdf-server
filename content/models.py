from django.db import models

from section.models import Section
from version.models import Version

# Create your models here
class Content(models.Model):
	section = models.ForeignKey(Section)
	version = models.ForeignKey(Version)
	text = models.TextField()
	
	def __str__(self):
		return self.section.title + ' - ' + self.version.id