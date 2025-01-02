from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # API REST
    path('api/<int:game_id>/start_countdown', views.game_start_countdown, name='game_start_countdown'),
    path('api/<int:game_id>/countdown_status', views.game_countdown_status, name='game_countdown_status'),
    path('api/bac/<int:game_id>/info', views.game_infos_little_bac, name='game_infos_little_bac'),
    path('api/bac/<int:game_id>/info_party', views.party_infos_little_bac, name='party_infos_little_bac'),
    path('api/bac/<int:game_id>/players', views.game_players_little_bac, name='game_players_little_bac'),
    path('api/bac/<int:game_id>/end_game', views.game_liitle_bac_end_game, name='end_game'),
    path('api/bac/<int:game_id>/player/<int:player_id>/toggle_ready', views.toggle_ready_status_little_bac, name='toggle_ready_status_little_bac'),


    path("", views.portal, name="portal_games"),
    path("bac", views.little_bac_home, name="bac_games"),
    path("bac/party", views.little_bac_start, name="bac_start_games"),
    path("bac/party/<str:party_id>", views.little_bac_party, name="bac_party_games"),
    path("bac/party/<str:party_id>/join", views.little_bac_party_join, name="bac_party_join_games"),
    path("bac/party/<str:party_id>/play", views.little_bac_party_play, name="bac_party_play_games"),
    path("bac/party/<str:party_id>/results", views.game_little_bac_results, name="bac_party_results_games"),

]