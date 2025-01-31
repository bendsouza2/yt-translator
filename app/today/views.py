"""Module for defining API views in the 'today' app"""
from typing import Optional

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import dateparse
from django.core import paginator

from today.models import Video
from today.serializers import VideoDetailsSerializer
from video_host.permissions import HasValidApiKey


class VideoDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for retrieving and manipulating VideoDetails instances

    Provides standard CRUD operations on Video data.
    """
    queryset = Video.objects.all()
    serializer_class = VideoDetailsSerializer

    @action(detail=False, methods=["get"], url_path="latest")
    def latest_video(self, request: Request) -> Response:
        """
        Fetches the most recently uploaded video
        :param request: the HTTP request - unused param
        :return: A JSON response with the latest video metadata and a 200 status code if successful, else 404 if no
        videos are available
        """
        recent_video = self.get_queryset().order_by("-upload_time").first()
        if recent_video is not None:
            serializer = self.get_serializer(recent_video)
            return Response(serializer.data)
        return Response({"detail": "No videos available"}, status=404)

    @action(detail=False, methods=["get"], url_path="paginated-videos")
    def paginated_videos(self, request: Request) -> Response:
        """
        Fetches videos within a specified date range and paginates the results.

        Query Parameters:
            - start_date (str, optional): Filter videos uploaded on or after this date (YYYY-MM-DD).
            - end_date (str, optional): Filter videos uploaded on or before this date (YYYY-MM-DD).
            - page_num (int, optional): The page number to fetch (default is 1).
            - limit (int, optional): The number of videos per page (default is 7).

        :param request: The HTTP request containing query parameters.
        :return: A JSON response containing paginated video data and metadata
        """
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        page_num = request.query_params.get("page_num", 1)
        limit = request.query_params.get("limit", 7)

        queryset = self.get_queryset()
        if start_date is not None:
            start_date_parsed = dateparse.parse_date(start_date)
            if start_date_parsed is not None:
                queryset = queryset.filter(upload_time__gte=start_date_parsed)
        if end_date is not None:
            end_date_parsed = dateparse.parse_date(end_date)
            if end_date_parsed is not None:
                queryset = queryset.filter(upload_time__lte=end_date_parsed)

        queryset = queryset.order_by("-upload_time")

        pages = paginator.Paginator(queryset, limit)
        try:
            videos_page = pages.page(page_num)
        except paginator.PageNotAnInteger:
            return Response({"detail": "Page number must be an integer"}, status=400)
        except paginator.EmptyPage:
            return Response({
                "videos": [],
                "detail": "Page number out of range - it's likely that no older videos are available",
                "total_videos": pages.count,
                "total_pages": pages.num_pages,
                "current_page": page_num,
                "has_next": False,
                "has_previous": False,
            }, status=200)

        serializer = self.get_serializer(videos_page, many=True)
        return Response({
            "videos": serializer.data,
            "total_videos": pages.count,
            "total_pages": pages.num_pages,
            "current_page": videos_page.number,
            "has_next": videos_page.has_next(),
            "has_previous": videos_page.has_previous(),
        })

    @action(detail=False, methods=["post"], url_path="write-to-db", permission_classes=[HasValidApiKey])
    def write_video_metadata(self, request: Request):
        """
        Verify the user has permission to write data to the DB, then write the video metadata to the MySQL RDS instance.

        This method checks if the incoming request contains valid video metadata. If valid, it either creates a new
        video record or updates an existing one in the database.

        :param request: The HTTP request containing a JSON with the video metadata to write to the DB.
        The JSON should include required fields such as 'video_id' and other relevant data.
        :return: A JSON response with a message indicating the status of the request to write to the DB.
        The response contains a success message and the appropriate HTTP status code based on the result:
                 - HTTP 201 CREATED if a new record was created.
                 - HTTP 200 OK if an existing record was updated.
                 - HTTP 400 BAD REQUEST if the data is invalid.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            video, created = Video.objects.update_or_create(
                video_id=serializer.validated_data["video_id"],
                defaults=serializer.validated_data
            )
            status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(
                {"message": f"{'Created' if created is True else 'Updated'} video record."},
                status=status_code,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
