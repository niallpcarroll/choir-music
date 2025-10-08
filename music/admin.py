from django.contrib import admin
from .models import MusicPiece, Recording

class RecordingAdmin(admin.ModelAdmin):
    list_display = ('music_piece', 'part', 'recording_file', 'recording_url', 'date_uploaded')

admin.site.register(MusicPiece)
admin.site.register(Recording, RecordingAdmin)


