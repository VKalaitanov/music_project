import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from main.models import Track
from .models import Playlist


class MyPlaylistView(ListView):
    template_name = 'my_playlists/my_playlists.html'
    context_object_name = 'playlist'

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)


@login_required
def add_track_to_playlist(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        playlist_id = data['playlist_id']
        track_id = data['track_id']

        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
        track = get_object_or_404(Track, id=track_id)

        if track not in playlist.tracks.all():
            playlist.tracks.add(track)
            return JsonResponse({'message': 'Трек добавлен в плейлист'})
        else:
            return JsonResponse({'message': 'Трек уже в плейлисте'})

    return JsonResponse({'message': 'Неверный запрос'})
