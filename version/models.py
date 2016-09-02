from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Version(models.Model):
	name = models.TextField(max_length=45)
	created_by = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name + ' - ' + self.id