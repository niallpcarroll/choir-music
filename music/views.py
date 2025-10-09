from django.shortcuts import render
from .models import MusicPiece

def music_list(request):
    pieces = MusicPiece.objects.all().order_by('title')
    print("DEBUG: pieces in view:", pieces)
    return render(request, 'music/music_list.html', {'pieces': pieces})
