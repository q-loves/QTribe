from django.urls import path

from pieces_info.views import UploadVideo, MyVideo,MyArticle,MyLife,UploadImage,PublishArticle,PlayVideo,StarVideo,TopVideo

urlpatterns=[
     path('upload_video/',UploadVideo.as_view()),
     path('my_video/',MyVideo.as_view()),
     path('play_video/',PlayVideo.as_view()),
     path('star_video/',StarVideo.as_view()),
     path('top_video/',TopVideo.as_view()),
     path('my_article/',MyArticle.as_view()),
     path('my_life/',MyLife.as_view()),
     path('upload_image/',UploadImage.as_view()),
     path('publish_article/', PublishArticle.as_view()),

]