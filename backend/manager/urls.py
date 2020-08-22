from django.urls import path
from .views import delete, add, promote

urlpatterns = [
  path('delete', delete),
  path('add', add),
  path('promote', promote)
]