"""Module for defining URL routing in the 'today' app - endpoints are created under the '/today/' path"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"videos", views.VideoDetailsViewSet, basename="videodetails")


urlpatterns = [
    path("today/", include(router.urls))
]
