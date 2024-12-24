from django.urls import path
from django.conf.urls.static import static

from passion_retro import settings
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("import", views.import_img, name="import"),
]