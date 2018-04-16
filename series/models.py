from django.db import models
from django.contrib.auth.models import User


class SeriesTable(models.Model):
    users = models.ManyToManyField(User)
    seriesID = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.seriesID)
