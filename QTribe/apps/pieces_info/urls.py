from django.urls import path

from pieces_info.views.article import MyArticle,  StarArticle, TopArticle, PublishArticle,DetailsArticle,DeleteArticle,CollectArticle,StarArticleList,ArticleSearchView,CollectArticleList
from pieces_info.views.life import MyLife,ShareLife,StarLife, TopLife, DetailsLife, DeleteLife, CollectLife, StarLifeList,LifeSearchView,CollectLifeList
from pieces_info.views.video import UploadVideo, MyVideo, PlayVideo, StarVideo, TopVideo, DeleteVideo,CollectVideo,StarVideoList,CollectVideoList,VideoSearchView

from pieces_info.views.comment import Comment_life

urlpatterns=[
     #视频
     path('upload_video/',UploadVideo.as_view()),
     path('my_video/',MyVideo.as_view()),
     path('play_video/',PlayVideo.as_view()),
     path('star_video/',StarVideo.as_view()),
     path('top_video/',TopVideo.as_view()),
     path('delete_video/',DeleteVideo.as_view()),
     path('collect_video/',CollectVideo.as_view()),
     path('star_video_list/',StarVideoList.as_view()),
     path('collect_video_list/',CollectVideoList.as_view()),
     path('search_video/',VideoSearchView()),
     #文章
     path('my_article/',MyArticle.as_view()),
     path('star_article/',StarArticle.as_view()),
     path('top_article/',TopArticle.as_view()),
     path('publish_article/', PublishArticle.as_view()),
     path('details_article/', DetailsArticle.as_view()),
     path('delete_article/', DeleteArticle.as_view()),
     path('collect_article/',CollectArticle.as_view()),
     path('star_article_list/',StarArticleList.as_view()),
     path('collect_article_list/',CollectArticleList.as_view()),
     path('search_article/',ArticleSearchView()),
     #生活
     path('my_life/',MyLife.as_view()),
     path('share_life/',ShareLife.as_view()),
     path('star_life/', StarLife.as_view()),
     path('top_life/', TopLife.as_view()),
     path('details_life/', DetailsLife.as_view()),
     path('delete_life/', DeleteLife.as_view()),
     path('collect_life/',CollectLife.as_view()),
     path('star_life_list/',StarLifeList.as_view()),
     path('collect_life_list/',CollectLifeList.as_view()),
     path('search_life/',LifeSearchView()),
     #评论
     path('comment_life/',Comment_life.as_view())

]