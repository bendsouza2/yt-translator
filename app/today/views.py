from django.shortcuts import render

from today.models import Video


def video_list(request):
    videos = Video.objects.all()
    return render(request, "videos/video_list.html", {"videos": videos})
