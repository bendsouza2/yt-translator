from django.urls import path
from . import views

urlpatterns = [
    path('latest-video/', views.latest_video, name='latest_video'),
]
