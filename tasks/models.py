from django.db import models
from boards.models import Board
from lists.models import List

# Create your models here.
class Task(models.Model):
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)
    list_id = models.ForeignKey(List, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000, blank=False, null=False)
    creatorEmail = models.CharField(max_length=255, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.body
