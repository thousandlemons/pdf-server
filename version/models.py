from django.contrib.auth.models import User
from django.db import models


class Version(models.Model):
    name = models.TextField()
    created_by = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s [%d]".format(self.name, self.id)
