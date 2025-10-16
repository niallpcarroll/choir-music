from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import MusicPiece, Recording, Movement

# --- Music Models ---


class MovementInline(admin.TabularInline):
    model = Movement
    extra = 1  # how many empty movement forms to show initially


@admin.register(MusicPiece)
class MusicPieceAdmin(admin.ModelAdmin):
    list_display = ("title", "composer", "date_added")
    search_fields = ("title", "composer")
    ordering = ("title",)  # Sort alphabetically by title
    inlines = [MovementInline]  # <-- added inline


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    search_fields = ("title", "music_piece__title")  # required for autocomplete


@admin.register(Recording)
class RecordingAdmin(admin.ModelAdmin):
    list_display = (
        "music_piece",
        "movement",
        "part",
        "recording_file",
        "recording_url",
        "date_uploaded",
    )
    search_fields = (
        "music_piece__title",
        "music_piece__composer",
        "movement__title",
        "part",
    )
    ordering = ("music_piece__title", "movement__order", "part")
    autocomplete_fields = ("music_piece", "movement")  # now works because Movement is registered


# --- User Admin Customization ---
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = ("username", "email", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined")
    actions = ["approve_users"]

    def approve_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} user(s) successfully approved.")

    approve_users.short_description = "Approve selected users"
