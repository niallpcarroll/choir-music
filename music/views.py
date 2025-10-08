from django.shortcuts import render
from .models import MusicPiece

def music_list(request):
    music_pieces = MusicPiece.objects.all().order_by('title')
    return render(request, 'music/music_list.html', {'music_pieces': music_pieces})
