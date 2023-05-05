from django.urls import path

from QTribe.apps.user.views import Register

urlpatterns=[
   path('register/',Register.as_view()),
]