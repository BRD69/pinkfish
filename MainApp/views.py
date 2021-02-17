from django.conf import settings
from django.shortcuts import render
from django.db.models import Q

from .models import *
from .common import common


def main(request):
    title = "Главная"
    weight_categories = WeightCategories.objects.all()
    banners = Banner.objects.filter(is_active=True)
    banners_is_active = True if len(banners) else False
    settings_app = SettingsApps.objects.first()
    fighters_top_5 = Fighters.objects.all()  # TODO: доделать ТОП-5
    content = {
        "title": title,
        "promotions": Promotions.objects.all(),
        "weight_categories": weight_categories,
        "banners": banners,
        "banners_is_active": banners_is_active,
        "media_url": settings.MEDIA_URL,
        "banners_visible": settings_app.banners_is_active,
        "video": Video.objects.last(),
        "podcasts": Podcasts.objects.order_by('-pk')[:5],
        "fighters_top_5": fighters_top_5,

    }
    return render(request, "MainApp/index.html", content)


def about(request):
    content = {}
    return render(request, "MainApp/about.html", content)


def news(request):
    content = {}
    return render(request, "MainApp/news.html", content)


def promotions(request):
    content = {}
    return render(request, "MainApp/index.html", content)


def promotion(request, pk):
    content = {}
    return render(request, "MainApp/index.html", content)


def fighters_get(request, pk=None):
    fighters_top_5 = Fighters.objects.all()  # TODO: доделать ТОП-5

    if pk:
        weight_category = WeightCategories.objects.get(pk=pk)
        selected_wc = weight_category.name
        fighters = Fighters.objects.filter(weight_category=weight_category).order_by("weight")
    else:
        search = request.GET.get("search", "")
        weight_category = request.GET.get("weight_category", "")
        selected_wc = "Все бойцы"
        if search:
            fighters = Fighters.objects.filter(Q(last_name__icontains=search) |
                                               Q(nickname__icontains=search) |
                                               Q(first_name__icontains=search))
        elif weight_category:
            if int(weight_category) == 0:
                fighters = Fighters.objects.all().order_by("weight_category")
            else:
                fighters = Fighters.objects.filter(weight_category=int(weight_category)).order_by("weight")
                selected_wc = WeightCategories.objects.get(pk=int(weight_category)).name
        else:
            fighters = Fighters.objects.all().order_by("weight_category")

    content = {
        "title": "Бойцы",
        "promotions": Promotions.objects.all(),
        "podcasts": Podcasts.objects.order_by('-pk')[:5],
        "media_url": settings.MEDIA_URL,
        "weight_categories": WeightCategories.objects.all(),
        "selected_wc": selected_wc,
        "fighters_top_5": fighters_top_5,
        "fighters": common.get_fighters_full_info(fighters)
    }
    return render(request, "MainApp/fighters.html", content)


def fighter_get(request, pk):
    fighter = Fighters.objects.get(pk=pk)
    content = {
        "title": f"{fighter}",
        "media_url": settings.MEDIA_URL,
        "promotions": Promotions.objects.all(),
        "weight_categories": WeightCategories.objects.all(),
        "podcasts": Podcasts.objects.order_by('-pk')[:5],
        "fighter": fighter,
        "battles": common.get_battles(fighter),
        "static_fighter": common.get_static_fighter(fighter),

    }
    return render(request, "MainApp/fighter.html", content)
