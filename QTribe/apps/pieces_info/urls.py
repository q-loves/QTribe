from django.urls import path

from QTribe.apps.pieces_info.views import UploadVideo

urlpatterns=[
     path('upload_video/',UploadVideo.as_view()),
]