# urls messagerie

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='pm_home'),
    path('view/<int:message_id>/', views.view_message, name='pm_view'),
    path('new/', views.new_message, name='pm_new'),
    path('delete/<int:message_id>/', views.delete_subject, name='pm_delete'),

    path('send_all_users/', views.send_all_users, name='pm_send_all_users'),
]
