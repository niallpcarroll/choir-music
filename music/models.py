from django.db import models

class MusicPiece(models.Model):
    title = models.CharField(max_length=200)
    composer = models.CharField(max_length=100, blank=True)
    sheet_music = models.FileField(upload_to="sheet_music/", blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("title", "composer")  # prevent duplicates with same composer

    def __str__(self):
        if self.composer:
            return f"{self.title} ({self.composer})"
        return self.title


# ----------------------------
# Movement MODEL
# ----------------------------
class Movement(models.Model):
    music_piece = models.ForeignKey(
        MusicPiece, on_delete=models.CASCADE, related_name="movements"
    )
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.music_piece.title} – {self.title}"

    class Meta:
        ordering = ['order']


# ----------------------------
# Recording MODEL (updated)
# ----------------------------
class Recording(models.Model):
    music_piece = models.ForeignKey(
        MusicPiece, on_delete=models.CASCADE, related_name="recordings"
    )
    movement = models.ForeignKey(
        Movement,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="recordings"
    )  # <-- new field to link recording to a movement
    part = models.CharField(max_length=50, blank=True)
    recording_file = models.FileField(upload_to="recordings/", blank=True, null=True)
    recording_url = models.URLField(blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.movement:
            return f"{self.music_piece.title} – {self.movement.title} ({self.part})"
        return f"{self.music_piece.title} ({self.part})"

    @property
    def part_initials(self):
        if not self.part:
            return ""
        part_lower = self.part.lower()
        if "soprano" in part_lower and "alto" in part_lower:
            return "S/A"
        elif "tenor" in part_lower and "bass" in part_lower:
            return "T/B"
        elif part_lower == "choir":
            return "Ch"
        elif "/" in self.part:
            return "/".join([p.strip()[0].upper() for p in self.part.split("/")])
        else:
            return self.part[0].upper()
