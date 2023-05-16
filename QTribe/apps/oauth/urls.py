from django.urls import path

from oauth.views import BindQQ,GetQQUrl

urlpatterns=[
    path('about/',BindQQ.as_view()),
    path('get_qq_url/',GetQQUrl.as_view()),

]