from django.urls import path
from .views import csrf, userLogin, register, userLogout, changePassword

urlpatterns = [
  path('csrf', csrf),
  path('login', userLogin),
  path('register', register),
  path('logout', userLogout),
  path('changepassword', changePassword)
]