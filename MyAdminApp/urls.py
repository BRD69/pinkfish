from django.urls import path, re_path

import MyAdminApp.views as adminapp

from .apps import MyadminappConfig

app_name = MyadminappConfig.name

urlpatterns = [
    path("", adminapp.main, name="main"),
    path("login/", adminapp.login, name="login"),
    path("logout/", adminapp.logout, name="logout"),
    path("banner/add/", adminapp.banner_add, name="banner_add"),
    path("banners/active/", adminapp.banners_is_active, name="banners_is_active"),
    path("image/<int:pk>/", adminapp.image, name="image"),
    path("video/save/", adminapp.video_save, name="video_save"),
    path("podcast/add/", adminapp.podcast_add, name="podcast_add"),
    path("battle/add/", adminapp.battle_add, name="battle_add"),
    path("users/", adminapp.users, name="users"),
    path("users/add/", adminapp.user_add, name="user_add"),
    path("users/update/<int:pk>/", adminapp.user_update, name="user_update"),
    path("fighters/", adminapp.fighters, name="fighters"),
    path("fighter/add/", adminapp.fighter_add, name="fighter_add"),
    path("fighter/update/<int:pk>/", adminapp.fighter_update, name="fighter_update"),
    path("others/", adminapp.others, name="others"),
    path("others/sports/add/", adminapp.object_add, name="sport_add"),
    path("others/promo/add/", adminapp.object_add, name="promotions_add"),
    path("others/clubs/add/", adminapp.object_add, name="clubs_add"),
    path("others/wc/add/", adminapp.wc_add, name="wc_add"),

]
