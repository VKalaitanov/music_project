from django.contrib import admin

from .models import Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    fields = []

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
