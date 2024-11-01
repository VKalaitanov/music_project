import datetime

from django.db import models
from mutagen import File as MutagenFile


class Category(models.Model):
    name = models.CharField('Название категории', max_length=100, unique=True)
    slug = models.SlugField('Слаг', max_length=100, unique=True)
    image = models.ImageField('Изображение категории', upload_to='category/', default=None, null=True)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Track(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='tracks/')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Проверяем, что аудиофайл загружен и длительность не задана
        if self.audio_file:
            # Открываем аудиофайл с помощью mutagen
            audio = MutagenFile(self.audio_file)
            if audio and audio.info:
                # Получаем длительность в секундах
                duration_in_seconds = int(audio.info.length)
                # Преобразуем в формат timedelta
                self.duration = datetime.timedelta(seconds=duration_in_seconds)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.audio_file:
            self.audio_file.delete(save=False)
        if self.cover_image:
            self.cover_image.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title
