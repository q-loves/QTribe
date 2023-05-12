from django.urls import path

from pieces_info.views import UploadVideo, MyVideo,MyArticle,MyLife

urlpatterns=[
     path('upload_video/',UploadVideo.as_view()),
     path('my_video/',MyVideo.as_view()),
     path('my_article/',MyArticle.as_view()),
     path('my_life/',MyLife.as_view()),
]