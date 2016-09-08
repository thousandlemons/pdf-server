from django.contrib.auth.models import User
from django.db import models


class Version(models.Model):
    name = models.TextField()
    owner = models.ForeignKey(User, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "[{id}] {name} by {owner}".format(name=self.name, id=self.id, owner=self.owner.username if self.owner else "default")

    def is_owned_by(self, user):
        return user == self.owner
