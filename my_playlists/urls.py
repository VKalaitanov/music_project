from django.urls import path
from . import views
app_name = 'playlists'

urlpatterns = [
    path('me/', views.MyPlaylistView.as_view()),
    path('add_track_to_playlist/', views.add_track_to_playlist, name='add_track_to_playlist'),
]
