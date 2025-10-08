from django.db import models

class MusicPiece(models.Model):
    title = models.CharField(max_length=200)
    composer = models.CharField(max_length=100, blank=True)
    sheet_music = models.FileField(upload_to='sheet_music/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Recording(models.Model):
    music_piece = models.ForeignKey(MusicPiece, on_delete=models.CASCADE, related_name='recordings')
    part = models.CharField(max_length=50, blank=True)  # e.g., "Soprano", "Alto", etc.
    recording_file = models.FileField(upload_to='recordings/', blank=True, null=True)
    recording_url = models.URLField(blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.music_piece.title} ({self.part})"
