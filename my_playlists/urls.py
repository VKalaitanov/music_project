from django.urls import path
from . import views

app_name = 'playlists'

urlpatterns = [
    path('me/', views.MyPlaylistView.as_view(), name='me'),  # все созданные плейлисты
    path('me/<int:playlist_pk>/', views.DetailMyPlaylistView.as_view(), name='me_pk'),  # для перехода в плейлист
    path('add_track_to_playlist/', views.add_track_to_playlist, name='add_track_to_playlist'),  # add track to playlist
    path('create/', views.CreatePlaylistView.as_view(), name='create_playlist'),  # для создания плейлиста
    path('update/<int:playlist_pk>/', views.UpdatePlaylistView.as_view(), name='update_playlist'),  # для обвноления плейлиста
    path('delete/<int:playlist_pk>/', views.DeletePlaylistView.as_view(), name='delete_playlist')  # для удаления плейлиста
]
