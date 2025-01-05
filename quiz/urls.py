from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='quiz_home'),
    path('<int:quiz_id>/', views.quiz, name='quiz'),
    path('result/<int:user_quiz_id>/', views.result, name='quiz_result'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('create/<int:quiz_id>/', views.create_responses_quiz, name='create_responses_quiz'),
]