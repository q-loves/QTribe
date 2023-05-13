from django.urls import path

from index.views import HomePage,NoFindPage,Information


urlpatterns=[
    path('home_index/',HomePage.as_view()),
    path('no_find/',NoFindPage.as_view()),

    path('information/',Information.as_view()),
]