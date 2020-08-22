from django.db import models
from django.conf import settings
import uuid

class Boards(models.Model):
  name = models.CharField(max_length=20)
  board_num = models.SmallIntegerField(unique=True)
  topic_sum = models.IntegerField(null=True)
  post_sum = models.IntegerField(null=True)
  last_post = models.ForeignKey('Posts', on_delete=models.SET_NULL, null=True, db_constraint=False)

class Topics(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  topic = models.CharField(max_length=30)
  creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, db_constraint=False)
  date = models.DateTimeField()
  topic_num = models.IntegerField()
  post_sum = models.IntegerField()
  last_post = models.ForeignKey('Posts', on_delete=models.SET_NULL, null=True, db_constraint=False)
  last_date = models.DateTimeField()
  board = models.ForeignKey('Boards', on_delete=models.SET_NULL, null=True, db_constraint=False)

class Posts(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  post = models.CharField(max_length=250)
  poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, db_constraint=False)
  date = models.DateTimeField()
  post_num = models.IntegerField()
  topic = models.ForeignKey('Topics', on_delete=models.CASCADE, null=True, db_constraint=False)
  last_date = models.DateTimeField(null=True)