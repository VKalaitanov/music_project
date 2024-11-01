import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from main.models import Track
from .models import Playlist
from .forms import CreatePlaylistForm


class MyPlaylistView(LoginRequiredMixin, ListView):
    template_name = 'my_playlists/my_playlists.html'
    context_object_name = 'playlist'

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)


class DetailMyPlaylistView(LoginRequiredMixin, DetailView):
    template_name = 'my_playlists/detail_my_playlists.html'
    context_object_name = 'playlist'
    model = Playlist

    def get_object(self, queryset=None):
        obj = get_object_or_404(Playlist, pk=self.kwargs['playlist_pk'], user=self.request.user)
        if not obj:
            raise Http404("Плейлист не найден")
        return obj


class CreatePlaylistView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = CreatePlaylistForm
    template_name = 'my_playlists/create_playlists.html'
    success_url = reverse_lazy('playlists:me')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.object.save()
        return response


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
