from django.db import models
from django.utils import timezone

# Create your models here.

class Pet(models.Model):
    name = models.CharField(max_length=200)
    species = models.CharField(max_length=200)
    age = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
