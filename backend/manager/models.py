from django.db import models
from django.conf import settings

class Permission(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  power = models.SmallIntegerField()

class Area(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  board_num = models.ForeignKey('forum.Boards', on_delete=models.CASCADE, to_field='board_num')