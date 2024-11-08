from django.shortcuts import render

from today.models import Video


def video_list(request):
    videos = Video.objects.all()
    return render(request, "videos/video_list.html", {"videos": videos})


def latest_video(request):
    recent_video = Video.objects.order_by('-upload_date').first()
    return render(request, 'videos/video_list.html', {'video': recent_video})
