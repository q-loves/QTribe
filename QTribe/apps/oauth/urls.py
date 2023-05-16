from django.urls import path

from oauth.views import BindQQ,GetQQUrl,GetWeChatUrl,BindWeChat

urlpatterns=[
    path('about/',BindQQ.as_view()),
    path('weixin/',BindWeChat.as_view()),
    path('get_qq_url/',GetQQUrl.as_view()),
    path('get_wechat_url/',GetWeChatUrl.as_view()),

]