from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse, HttpResponseRedirect
import json

class LoginVerify(MiddlewareMixin):
  def process_request(self, request):
    verify = request.user.is_authenticated
    if request.path == '/':
      if verify:
        response = render(request, 'index.html')
        response.set_cookie('isLogin', 1)
        response.set_cookie('username', json.dumps(request.user.username))

        permission = request.user.permission_set.all()
        if permission:
          power = permission.get().power
          area = request.user.area_set.all()
          area_arr = []
          for a in area:
            # board_num_id is ForeignKey board_num
            area_arr.append(a.board_num_id)
          response.set_cookie('power', power)
          response.set_cookie('area', area_arr)

        return response
    elif request.path == '/user/login' or request.path == '/user/register':
      pass
    #The development environment to verify identity
    elif request.path == '/getlogincookies':
      if request.method == 'POST':
        code = json.loads(request.body).get('code')
        if verify and code == 1:
          response = JsonResponse({})
          response.set_cookie('isLogin', 1)
          response.set_cookie('username', json.dumps(request.user.username))
          
          permission = request.user.permission_set.all()
          if permission:
            power = permission.get().power
            area = request.user.area_set.all()
            area_arr = []
            for a in area:
              # board_num_id is ForeignKey board_num
              area_arr.append(a.board_num_id)
            response.set_cookie('power', power)
            response.set_cookie('area', area_arr)

          return response
        else:
          return JsonResponse({})
      else:
        return HttpResponseRedirect('/')
    else:
      if not verify:
        return HttpResponseRedirect('/')