from django.urls import path
from . import views
app_name = 'playlists'

urlpatterns = [
    path('me/', views.MyPlaylistView.as_view(), name='me'),
    path('me/<int:playlist_pk>/', views.DetailMyPlaylistView.as_view(), name='me_pk'),
    path('add_track_to_playlist/', views.add_track_to_playlist, name='add_track_to_playlist'),
    path('create/', views.CreatePlaylistView.as_view())
]
