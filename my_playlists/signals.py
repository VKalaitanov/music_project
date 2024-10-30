from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Playlist


@receiver(m2m_changed, sender=Playlist.tracks.through)
def update_tracks_count(sender, instance, **kwargs):
    instance.tracks_count = instance.tracks.count()
    instance.save()
