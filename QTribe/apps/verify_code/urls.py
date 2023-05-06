from django.urls import re_path

from verify_code.views import SendSmsCode,CheckSmsCode


urlpatterns=[
    re_path('send_smscode/(?P<phone>1[3,5,7,8,9]\d{9})/',SendSmsCode.as_view()),
    re_path('check_smscode/(?P<phone>1[3,5,7,8,9]\d{9})/',CheckSmsCode.as_view()),
]