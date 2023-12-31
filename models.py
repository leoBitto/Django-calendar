# models.py

from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField()
    end_time = models.TimeField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title
