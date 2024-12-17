from django.urls import path
from django.conf.urls.static import static

from passion_retro import settings
from . import views

urlpatterns = [
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("profile/<str:user_id>/", views.another_profile, name="profile"),
    path("profile/update/", views.profile_update, name="profile_update"),
    path("contribute/", views.contribute, name="contribute"),
    path("contribute/<str:type>/", views.form_contribute, name="form_contribute"),
]