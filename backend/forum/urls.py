from django.urls import path
from .views import forum_data, board_data, topic_data, add_topic, add_post, delete_topic, delete_post, update_post

urlpatterns = [
  path('forumdata/', forum_data),
  path('<int:board_num>/', board_data),
  path('<int:board_num>/<int:topic_num>/', topic_data),
  path('addtopic', add_topic),
  path('addpost', add_post),
  path('deletetopic', delete_topic),
  path('deletepost', delete_post),
  path('updatepost', update_post)
]