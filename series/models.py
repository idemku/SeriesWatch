##
# @file
# File documentation
#

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    emailNotify = models.BooleanField(default=False)


class SeriesTable(models.Model):
    users = models.ManyToManyField(User)
    seriesID = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.seriesID)
