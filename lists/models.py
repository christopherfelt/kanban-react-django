from django.db import models
from boards.models import Board


class List(models.Model):
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    color = models.CharField(max_length=10, default="#ccc")
    creatorEmail = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.title