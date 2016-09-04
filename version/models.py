from django.contrib.auth.models import User
from django.db import models


class Version(models.Model):
    name = models.TextField()
    created_by = models.ForeignKey(User, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{name} [{id}]".format(name=self.name, id=self.id)
