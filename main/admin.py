from django.contrib import admin
from .models import Category, Artist, Track, TrackImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)


class TrackImageInline(admin.TabularInline):
    model = TrackImage
    extra = 1  # Количество дополнительных полей для загрузки


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'category', 'duration', 'created_at')
    search_fields = ('title', 'artist__name')
    list_filter = ('artist', 'category')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('artist', 'category')
    inlines = [TrackImageInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'artist', 'category', 'audio_file')
        }),
        ('Дополнительная информация', {
            'fields': ('created_at',),
        }),
    )
