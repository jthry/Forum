from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from forum.models import Boards, Topics, Posts
from manager.models import Permission, Area
from django.db.models import Max
from django.db import transaction
from django.db import connection
import json

@transaction.atomic
def delete(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    board_num = data.get('board_num')
    topic_num = data.get('topic_num')
    post_num = data.get('post_num')
    
    permission = request.user.permission_set.all()
    if permission:
      power = permission.get().power
      area = request.user.area_set.all()
      area_arr = []
      for a in area:
        # board_num_id is ForeignKey board_num
        area_arr.append(a.board_num_id)
    else:
      power = 0
      area_arr = []

    board = Boards.objects.get(board_num = board_num)
    if topic_num == None:
      if board_num % 100 == 0:
        if not Boards.objects.raw('SELECT id FROM forum_boards WHERE board_num LIKE %s AND board_num > %s limit 1', [str(board_num // 100) + '__', board_num]):
          board.delete()
      elif not Topics.objects.filter(board = board).exists():
        board.delete()
    elif post_num == None:
      topic = Topics.objects.get(board = board, topic_num = topic_num)
      if board.board_num in area_arr or power > 1000:
        creator = topic.creator
        creator_permission = creator.permission_set.all()
        if creator_permission:
          creator_power = creator_permission.get().power
        else:
          creator_power = 0
        if power > creator_power:
          board.topic_sum = board.topic_sum - 1
          board.post_sum = board.post_sum - topic.post_sum
          board.save()
          topic.delete()
    else:
      topic = Topics.objects.get(board = board, topic_num = topic_num)
      post = Posts.objects.get(topic = topic, post_num = post_num)
      if post.post_num == 1:
        return
      if board.board_num in area_arr or power > 1000:
        poster = post.poster
        poster_permission = poster.permission_set.all()
        if poster_permission:
          poster_power = poster_permission.get().power
        else:
          poster_power = 0
        creator = topic.creator
        if request.user == creator and power == 0:
          power += 10
        if power > poster_power:
          topic.post_sum = topic.post_sum - 1
          topic.save()
          board.post_sum = board.post_sum - 1
          board.save()
          post.delete()

    return JsonResponse({
      'code': 1
    })

def add(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    container_name = data.get('container_name')
    board_name = data.get('board_name')

    permission = request.user.permission_set.all()
    if permission:
      power = permission.get().power
    else:
      power = 0
    
    if container_name != None and power > 1000:
      try:          
        with transaction.atomic():
          container = Boards.objects.filter(name = container_name, board_num__endswith = '00')
          if not container:
            board_max = Boards.objects.filter(board_num__endswith = '00').aggregate(Max('board_num'))['board_num__max']
            new_board_num = board_max + 100 if board_max else 100
            new_container = Boards(
              name = container_name,
              board_num = new_board_num,
              topic_sum = None,
              post_sum = None,
              last_post = None
            )
            new_container.save()

            if board_name != None:
              board = Boards(
                name = board_name,
                board_num = new_container.board_num + 1,
                topic_sum = 0,
                post_sum = 0,
                last_post = None
              )
              board.save()

          elif container and board_name != None:
            container = container.get()
            if container.board_num % 100 == 0:
              boards = [(board.name, board.board_num) for board in Boards.objects.raw('SELECT id, name, board_num FROM forum_boards WHERE board_num LIKE %s', [str(container.board_num // 100) + '__'])]
              boards = [[i[0] for i in boards], [i[1] for i in boards]]
              if board_name not in boards[0]:
                board_max = max(boards[1])
                new_board_num = board_max + 1
                board = Boards(
                  name = board_name,
                  board_num = new_board_num,
                  topic_sum = 0,
                  post_sum = 0,
                  last_post = None
                )
                board.save()

      except:
        transaction.rollback()
        return
      transaction.commit()

    return JsonResponse({
      'code': 1
    })

def promote(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    board_num = data.get('board_num')
    topic_num = data.get('topic_num')
    post_num = data.get('post_num')

    permission = request.user.permission_set.all()
    if permission:
      power = permission.get().power
    else:
      power = 0

    if power > 1000:
      board = Boards.objects.get(board_num = board_num)
      topic = Topics.objects.get(board = board, topic_num = topic_num)
      post = Posts.objects.get(topic = topic, post_num = post_num)
      try:          
        with transaction.atomic():
          poster = post.poster
          poster_permission = poster.permission_set.all()
          if not poster_permission:
            poster_permission = Permission(
              user = poster,
              power = 200
            )
            poster_permission.save()
            area = Area(
              user = poster,
              board_num = board
            )
            area.save()

      except:
        raise
        transaction.rollback()
        return
      transaction.commit()

      return JsonResponse({
        'code': 1
      })