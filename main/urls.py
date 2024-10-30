from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('track/<int:pk>/', views.DetailTrack.as_view(), name='detail_track'),
    path('category/<slug:slug>/', views.TrackListView.as_view(), name='track_list_by_category'),
    path('load-tracks/<slug>/', views.load_tracks, name='load_tracks'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
]
