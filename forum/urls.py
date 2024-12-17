from django.urls import path
from django.conf.urls.static import static

from passion_retro import settings
from . import views

urlpatterns = [
    path("", views.forum_home, name="forum_home"),
    path("<int:forum_id>/", views.topic_list, name="topic_list"),
    path("<int:forum_id>/create_topic/", views.create_topic, name="create_topic"),
    path("<int:forum_id>/<int:topic_id>/", views.topic_detail, name="post_list"),

    path("<int:topic_id>/lock/", views.lock_topic, name="lock_topic"),
    path("<int:topic_id>/unlock/", views.unlock_topic, name="unlock_topic"),
    path("<int:forum_id>/<int:topic_id>/deactivate/", views.deactivate_topic, name="deactivate_topic"),
    path("<int:forum_id>/<int:topic_id>/activate/", views.activate_topic, name="activate_topic"),
    path("<int:post_id>/deactivate/", views.deactivate_post, name="deactivate_post"),
    path("<int:post_id>/activate/", views.activate_post, name="activate_post"),
]