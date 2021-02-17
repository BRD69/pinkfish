from django.urls import path, re_path

import MainApp.views as mainapp

from .apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", mainapp.main, name="main"),
    path("about/", mainapp.about, name="about"),
    path("news/", mainapp.news, name="news"),
    path("promotions/", mainapp.promotions, name="promotions"),
    path("promotion/<int:pk>/", mainapp.promotion, name="promotion"),
    path("fighters/", mainapp.fighters_get, name="fighters"),
    path("fighters/<int:pk>/", mainapp.fighters_get, name="fighters_pk"),
    path("fighter/<int:pk>/", mainapp.fighter_get, name="fighter"),
]