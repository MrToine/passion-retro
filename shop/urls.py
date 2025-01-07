from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='shop_home'),
    path('buy/<int:item_id>/', views.buy, name='shop_buy'),
]