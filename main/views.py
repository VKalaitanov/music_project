from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView

from my_playlists.models import Playlist
from .models import Track, Category


# Create your views here.
class HomePage(ListView):
    model = Track
    template_name = 'main/index.html'
    context_object_name = 'tracks'  # Контекстное имя для списка треков
    title_page = 'Главная страница'

    def get_queryset(self):
        """Возвращает список треков"""
        return Track.objects.select_related('artist', 'category').all()

    def get_context_data(self, **kwargs):
        """Добавляем дополнительные данные в контекст"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['title_page'] = self.title_page
        context['playlists'] = \
            Playlist.objects.filter(user=self.request.user) if self.request.user.is_authenticated else None
        return context


class TrackListView(ListView):
    model = Track
    template_name = 'main/category.html'
    context_object_name = 'tracks'

    def get_queryset(self):
        """Возвращает список треков для выбранной категории"""
        slug = self.kwargs.get('slug')
        return Track.objects.filter(category__slug=slug).select_related('artist', 'category')

    def get_context_data(self, **kwargs):
        """Добавляем дополнительные данные в контекст"""
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs.get('slug'))
        return context


class DetailTrack(DetailView):
    model = Track
    template_name = 'main/detail_track.html'
    context_object_name = 'track'


def load_tracks(request, slug):
    tracks = Track.objects.filter(category__slug=slug).select_related('artist', 'category')
    track_list = []

    for track in tracks:
        track_list.append({
            'id': track.id,
            'title': track.title,
            'artist': track.artist.name,
            'cover_image': track.cover_image.url,
            'is_authenticated': request.user.is_authenticated,
            'login_url': reverse('users:login'),
            'track_url': reverse('main:detail_track', args=[track.id])  # Добавлено
        })

    return JsonResponse({'tracks': track_list})


def about(request):
    return render(request, 'main/about.html', {'title': 'Страница про нас'})


def contacts(request):
    return render(request, 'main/contacts.html', {'title': 'Страница контакты'})
