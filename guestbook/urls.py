from django.urls import path
from django.conf.urls.static import static

from passion_retro import settings
from . import views

urlpatterns = [
    path("", views.guestbook_home, name="guestbook_home"),
]