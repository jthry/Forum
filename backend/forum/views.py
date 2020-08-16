from django.shortcuts import render
from forum import models
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Max
from django.utils import timezone
import json
import datetime
import uuid

def forum_data(request):
  data = models.Boards.objects.all().values('name', 'board_num', 'topic_sum', 'post_sum', 'last_post')
  forum_data = []

  for board in data:
    #if num is multiples of 100, the board is a container
    if board['board_num']%100 == 0:
      del board['topic_sum']
      del board['post_sum']

    if board['last_post'] != None:
      post = models.Posts.objects.filter(id = board['last_post'])
      if post.exists():
        post = post.values('poster', 'date', 'post_num', 'topic')[0]
        post.update({
          'last_poster': post.pop('poster'),
          'last_date': post.pop('date').isoformat(),
          'last_post_num': post.pop('post_num'),
          'last_topic': post.pop('topic')
        })

        poster = User.objects.filter(id = post['last_poster'])
        try:
          poster = poster.values('username')[0]
          post['last_poster'] = poster['username']
        except IndexError:
          del post['last_poster']

        topic = models.Topics.objects.filter(id = post['last_topic'])
        try:
          topic = topic.values('topic', 'topic_num')[0]
          post['last_topic'] = topic['topic']
          post['last_topic_num'] = topic['topic_num']
        except IndexError:
          del post['last_topic']

        board.update(post)

    del board['last_post']
    forum_data.append(board)

  return JsonResponse({
    'forum_data': forum_data
  })

def board_data(request, board_num):
  page = int(request.GET.get('page') or 1)
  board_num = board_num

  board = models.Boards.objects.filter(board_num = board_num).values('id', 'name', 'topic_sum', 'post_sum')[0]
  Topics = models.Topics.objects.filter(board = board['id']).order_by('-last_date')[20*(page-1) : 20*page] \
      .values('topic', 'creator', 'date', 'topic_num', 'post_sum', 'last_post', 'last_date')
  del board['id']
  board_data = []

  for data in Topics:
    creator = User.objects.filter(id = data['creator']).values('username')[0]
    data['creator'] = creator['username']

    post = models.Posts.objects.filter(id = data['last_post']).values('poster', 'post_num')
    try:
      data.update(post[0])
      poster = User.objects.filter(id = data['poster']).values('username')[0]
      data['poster'] = poster['username']
    except IndexError:
      pass
    del data['last_post']

    board_data.append(data)

  return JsonResponse({
    'board_information': board,
    'board_data': board_data
  })

def topic_data(request, board_num, topic_num):
  page = int(request.GET.get('page') or 1)
  board_num = board_num
  topic_num = topic_num

  board = models.Boards.objects.filter(board_num = board_num).values('id')[0]
  topic = models.Topics.objects.filter(board = board['id'], topic_num = topic_num) \
      .values('id', 'creator', 'topic', 'post_sum')[0]
  post = models.Posts.objects.filter(topic = topic['id']).order_by('post_num')[20*(page-1) : 20*page] \
      .values('post', 'poster', 'date', 'post_num', 'last_date')
  del topic['id']
  post_data = []
  
  for data in post:
    try:
      poster = User.objects.filter(id = data['poster']).values('username')[0]
      poster_id = data['poster']
      data['poster'] = poster['username']
    except IndexError:
      del data['poster']

    if poster_id == topic['creator']:
      data['is_creator'] = True
    post_data.append(data)
  del topic['creator']

  return JsonResponse({
    'topic_information': topic,
    'post_data': post_data
  })

def add_topic(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    board_num = data.get('board_num')
    topic = data.get('topic')
    post = data.get('post')

    board = models.Boards.objects.filter(board_num = board_num)[0]
    board.topic_sum = board.topic_sum + 1
    board.post_sum = board.post_sum + 1

    topic_id = uuid.uuid4()
    post_id = uuid.uuid4()
    if models.Topics.objects.filter(id = topic_id).exists() or \
        models.Posts.objects.filter(id = post_id).exists():
      return
    
    creator = request.user
    date = timezone.now()
    topic_max = models.Topics.objects.filter(board = board.id).aggregate(Max('topic_num'))['topic_num__max']
    if topic_max:
      topic_num = topic_max + 1
    else:
      topic_num = 1
    add_topic = models.Topics(
      id = topic_id,
      topic = topic,
      creator = creator,
      date = date,
      topic_num = topic_num,
      post_sum = 1,
      last_post = None,
      last_date = date,
      board = board
    )
    
    add_post = models.Posts(
      id = post_id,
      post = post,
      poster = creator,
      date = date,
      post_num = 1,
      topic = add_topic,
      last_date = None
    )
    
    add_topic.last_post = add_post
    board.last_post = add_post

    try:
      with transaction.atomic():
        board.save()
        add_topic.save()
        add_post.save()
    except:
      transaction.rollback()
      return
    transaction.commit()

    return JsonResponse({
      'board_num': board_num,
      'topic_num': topic_num
    })

def add_post(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    board_num = data.get('board_num')
    topic_num = data.get('topic_num')
    post = data.get('post')

    board = models.Boards.objects.filter(board_num = board_num)[0]
    board.post_sum = board.post_sum + 1
    topic = models.Topics.objects.filter(topic_num = topic_num)[0]
    topic.post_sum = topic.post_sum + 1
    
    poster = request.user
    date = timezone.now()
    post_max = models.Posts.objects.filter(topic = topic.id).aggregate(Max('post_num'))
    post_num = post_max['post_num__max'] + 1
    add_post = models.Posts(
      post = post,
      poster = poster,
      date = date,
      post_num = post_num,
      topic = topic,
      last_date = None
    )

    board.last_post = add_post
    topic.last_post = add_post
    topic.last_date = date

    try:
      with transaction.atomic():
        board.save()
        topic.save()
        add_post.save()
    except:
      transaction.rollback()
      return
    transaction.commit()

    return JsonResponse({
      'code': 1
    })

def delete_topic(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    board_num = data.get('board_num')
    topic_num = data.get('topic_num')
    page = data.get('page')

    board = models.Boards.objects.filter(board_num = board_num)[0]
    topic = models.Topics.objects.filter(board = board.id, topic_num = topic_num)[0]

    if topic.creator == request.user:
      board.topic_sum -= 1
      board.post_sum -= topic.post_sum
      try:
        with transaction.atomic():
          board.save()
          topic.delete()
      except:
        transaction.rollback()
        return
      transaction.commit()

      request.method = 'GET'
      request.GET = request.GET.copy()
      request.GET['page'] = page
      return board_data(request, board_num)

    else:
      return

def delete_post(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    board_num = data.get('board_num')
    topic_num = data.get('topic_num')
    post_num = data.get('post_num')
    page = data.get('page')

    board = models.Boards.objects.filter(board_num = board_num)[0]
    topic = models.Topics.objects.filter(board = board.id, topic_num = topic_num)[0]
    post = models.Posts.objects.filter(topic = topic.id, post_num = post_num)[0]

    if post.poster == request.user:
      board.post_sum -= 1
      topic.post_sum -= 1
      try:
        with transaction.atomic():
          board.save()
          topic.save()
          post.delete()
      except:
        transaction.rollback()
        return
      transaction.commit()

      request.method = 'GET'
      request.GET = request.GET.copy()
      request.GET['page'] = page
      return topic_data(request, board_num, topic_num)

    else:
      return

def update_post(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    board_num = data.get('board_num')
    topic_num = data.get('topic_num')
    page = data.get('page')
    post_num = data.get('post_num')
    post_content = data.get('post')

    board = models.Boards.objects.filter(board_num = board_num)[0]
    topic = models.Topics.objects.filter(board = board.id, topic_num = topic_num)[0]
    post = models.Posts.objects.filter(topic = topic.id, post_num = post_num)[0]
    
    if post.poster == request.user:
      post.post = post_content
      post.last_date = timezone.now()
      board.last_post = post
      try:
        with transaction.atomic():
          board.save()
          post.save()
      except:
        transaction.rollback()
        return
      transaction.commit()

      request.method = 'GET'
      request.GET = request.GET.copy()
      request.GET['page'] = page
      return topic_data(request, board_num, topic_num)

    else:
      return