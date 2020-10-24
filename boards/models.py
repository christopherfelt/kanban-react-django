from django.db import models

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=False, null=False)
    creatorEmail = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.title