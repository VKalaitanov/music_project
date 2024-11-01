from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Playlist


class CRUDMixinPlaylist(LoginRequiredMixin):
    model = Playlist
    template_name = None
    context_object_name = 'playlist'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Playlist, pk=self.kwargs['playlist_pk'], user=self.request.user)  # type: ignore
        if not obj:
            raise Http404("Плейлист не найден")
        return obj
