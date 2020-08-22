from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from manager.models import Permission, Area
import json

def csrf(request):
  get_token(request)

def userLogin(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user = authenticate(request, username=username, password=password)
    if user:
      data = {
        'code': 1,
      }
      permission = user.permission_set.all()
      if permission:
        power = permission.get().power
        area = user.area_set.all()
        area_arr = []
        for a in area:
          # board_num_id is ForeignKey board_num
          area_arr.append(a.board_num_id)
        data['power'] = power
        data['area'] = area_arr

      login(request, user)
      return JsonResponse(data)
    else:
      return JsonResponse({
        'status': 0
      })

def register(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if User.objects.filter(username=username):
      return JsonResponse({
        'code': 0
      })
    else:
      user = User.objects.create_user(username=username, password=password)
      user.save()
      return JsonResponse({
        'code': 1
      })

def userLogout(request):
  if request.method == 'POST':
    logout(request)

    response = JsonResponse({'code': 1})
    return response

def changePassword(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    user = authenticate(request, username=request.user.username, password=old_password)
    if user:
      user.set_password(new_password)
      user.save()
    
    return userLogout(request)