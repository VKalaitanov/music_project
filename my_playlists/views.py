import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from main.models import Track
from .forms import CreatePlaylistForm, UpdatePlaylistForm
from .mixin import CRUDMixinPlaylist
from .models import Playlist


class MyPlaylistView(LoginRequiredMixin, ListView):
    template_name = 'my_playlists/my_playlists.html'
    context_object_name = 'playlist'

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_form'] = CreatePlaylistForm()  # Добавляем форму создания
        return context

    def post(self, request, *args, **kwargs):
        create_form = CreatePlaylistForm(request.POST)
        if create_form.is_valid():
            playlist = create_form.save(commit=False)
            playlist.user = request.user  # Привязываем пользователя к новому плейлисту
            playlist.save()
            return redirect('playlists:me')  # Обновляем страницу после создания
        else:
            return self.get(request, create_form=create_form)  # Отобразим ошибки формы


class DetailMyPlaylistView(CRUDMixinPlaylist, DetailView):
    model = Playlist
    form_class = UpdatePlaylistForm
    template_name = 'my_playlists/detail_my_playlists.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = get_object_or_404(Playlist, pk=self.kwargs['playlist_pk'])
        context['update_form'] = kwargs.get('update_form', self.form_class(instance=playlist))
        return context

    def post(self, request, *args, **kwargs):
        playlist = get_object_or_404(Playlist, pk=self.kwargs['playlist_pk'])
        update_form = self.form_class(request.POST, instance=playlist)

        if update_form.is_valid():
            update_form.save()
            return redirect(reverse('playlists:me_pk', args=[playlist.pk]))
        else:
            # Устанавливаем self.object, чтобы избежать AttributeError
            self.object = playlist
            return self.render_to_response(self.get_context_data(update_form=update_form))

class CreatePlaylistView(CRUDMixinPlaylist, CreateView):
    form_class = CreatePlaylistForm
    template_name = 'my_playlists/create_playlists.html'
    success_url = reverse_lazy('playlists:me')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.object.save()
        return response

    def get_object(self, queryset=None):
        pass


class UpdatePlaylistView(CRUDMixinPlaylist, UpdateView):
    form_class = UpdatePlaylistForm
    template_name = 'my_playlists/update_playlist.html'

    def get_success_url(self):
        return reverse_lazy('playlists:me')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Убедимся, что только владелец может обновить трек
        return super().form_valid(form)


class DeletePlaylistView(CRUDMixinPlaylist, DeleteView):
    template_name = 'my_playlists/delete_playlist.html'
    success_url = reverse_lazy('playlists:me')

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

@login_required
@require_POST
def remove_track_from_playlist(request):
    data = json.loads(request.body)
    playlist_id = data.get('playlist_id')
    track_id = data.get('track_id')

    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    track = get_object_or_404(Track, id=track_id)

    if track in playlist.tracks.all():
        playlist.tracks.remove(track)
        return JsonResponse({'message': 'Трек удален из плейлиста'})
    else:
        return JsonResponse({'message': 'Трек не найден в плейлисте'}, status=400)