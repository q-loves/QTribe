from django.urls import path

from index.views import HomePage,NoFindPage,Information,VideoMall, ArticleMall,LifeMall,OtherUser,StartIt


urlpatterns=[
    path('home_index/',HomePage.as_view()),
    path('start_it/',StartIt.as_view()),
    path('no_find/',NoFindPage.as_view()),

    path('information/',Information.as_view()),
    path('video_mall/',VideoMall.as_view()),
    path('article_mall/',ArticleMall.as_view()),
    path('life_mall/',LifeMall.as_view()),
    path('other_user/',OtherUser.as_view()),

]