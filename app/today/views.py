from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from today.models import Video
from today.serializers import VideoDetailsSerializer


class VideoDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for retrieving and manipulating VideoDetails instances

    Provides standard CRUD operations on Video data.
    """
    queryset = Video.objects.all()
    serializer_class = VideoDetailsSerializer

    @action(detail=False, methods=["get"], url_path="latest")
    def latest_video(self, request):
        recent_video = self.get_queryset().order_by("-upload_date").first()
        if recent_video is not None:
            serializer = self.get_serializer(recent_video)
            return Response(serializer.data)
        return Response({"detail": "No videos available"}, status=404)
