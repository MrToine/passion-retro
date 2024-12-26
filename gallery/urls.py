from django.urls import path
from django.conf.urls.static import static

from passion_retro import settings
from . import views

urlpatterns = [
    path("", views.home_gallery, name="home_gallery"),
    path("import", views.import_img, name="import"),
]