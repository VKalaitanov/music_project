from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from main.models import Track


class Playlist(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='playlists')
    tracks = models.ManyToManyField(Track, related_name='playlists', blank=True)
    tracks_count = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('playlists:me_pk', kwargs={'playlist_pk': self.pk})
