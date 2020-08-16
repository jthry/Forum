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
          return response
        else:
          return JsonResponse({})
      else:
        return HttpResponseRedirect('/')
    else:
      if not verify:
        return HttpResponseRedirect('/')