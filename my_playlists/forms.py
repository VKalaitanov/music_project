from django import forms
from .models import Playlist


class CreatePlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title']


class UpdatePlaylistForm(CreatePlaylistForm):
    class Meta(CreatePlaylistForm.Meta):
        pass
