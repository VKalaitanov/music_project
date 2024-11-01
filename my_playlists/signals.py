from django.db.models.signals import m2m_changed, pre_delete
from django.dispatch import receiver

from main.models import Track
from .models import Playlist


@receiver(m2m_changed, sender=Playlist.tracks.through)
def update_tracks_count(sender, instance, **kwargs):
    instance.tracks_count = instance.tracks.count()
    instance.save()


@receiver(pre_delete, sender=Track)
def update_playlist_tracks_count(sender, instance, **kwargs):
    playlists = instance.playlists.all()
    for playlist in playlists:
        playlist.tracks_count -= 1
        playlist.save()
