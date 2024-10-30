from django.contrib import admin

from .models import Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    fields = []
    filter_horizontal = ['tracks']
