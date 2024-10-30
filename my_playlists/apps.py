from django.apps import AppConfig


class MyPlaylistsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_playlists'

    def ready(self):
        from . import signals  # type: ignore
