from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

from MainApp.models import *
from MyAdminApp.forms import *
from MyAdminApp.common import common


def login(request):
    login_form = UserForm(data=request.POST or None)
    if request.method == "POST" and login_form.is_valid():
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse("myadmin:main"))

    content = {"title": "Вход", "login_form": login_form}
    return render(request, "MyAdminApp/login.html", content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("myadmin:main"))


# Главная
@login_required()
def main(request):
    settings_app = SettingsApps.objects.first()
    video = Video.objects.last()
    content = {
        "title": "Админка",
        "active_menu": "main",
        "media_url": settings.MEDIA_URL,
        "banners": Banner.objects.all(),
        "form_banners": BannersForm,
        "banners_is_active": settings_app.banners_is_active,
        "form_video": VideoForm(instance=video),
        "podcasts": Podcasts.objects.all(),
        "form_podcast": PodcastsForm,
        "battles": Fights.objects.all(),
        "form_battle": BattleForm,
        "user": request.user,
    }
    return render(request, "MyAdminApp/index.html", content)


@login_required()
def banners_is_active(request):
    settings_app = SettingsApps.objects.first()
    if request.method == "GET":
        if 'status_banner' in request.GET:
            settings_app.banners_is_active = True
        else:
            settings_app.banners_is_active = False
    settings_app.save()
    return HttpResponseRedirect(reverse("MyAdminApp:main"))


@login_required()
def banner_add(request):
    if request.method == "POST":
        form = BannersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse("MyAdminApp:main"))


@login_required()
def image(request, pk):
    banner = Banner.objects.get(pk=pk)
    if request.method == "GET":
        banner_form = BannersForm(instance=banner)
    else:
        banner_form = BannersForm(request.POST, instance=banner)
        banner_form.save()
        return HttpResponseRedirect(reverse("MyAdminApp:main"))

    content = {
        "title": "Баннер",
        "media_url": settings.MEDIA_URL,
        "banner": banner,
        "banner_form": banner_form,
    }
    return render(request, "MyAdminApp/image.html", content)


@login_required()
def video_save(request):
    if request.method == "POST":
        form = VideoForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse("MyAdminApp:main"))


@login_required()
def podcast_add(request):
    if request.method == "POST":
        form = PodcastsForm(request.POST)
        if form.is_valid():
            HTML_code = request.POST['HTML_code']
            name = request.POST['name']
            src, href, desc = common.get_info_podcast(HTML_code)
            podcast = Podcasts(
                name=name,
                HTML_code=HTML_code,
                src=src, href=href,
                description=desc
            )
            podcast.save()
    return HttpResponseRedirect(reverse("MyAdminApp:main"))


@login_required()
def battle_add(request):
    if request.method == "POST":
        fighter_1 = Fighters.objects.get(pk=int(request.POST['fighter1']))
        fighter_2 = Fighters.objects.get(pk=int(request.POST['fighter2']))
        if int(request.POST['winner']) == 1:
            winner = fighter_1
        else:
            winner = fighter_2
        date = request.POST["date"]
        promotion = Promotions.objects.get(pk=int(request.POST["promotion"]))
        link = request.POST["link"]
        Fights(fighter1=fighter_1,
               fighter2=fighter_2,
               winner=winner,
               date=date,
               promotion=promotion,
               link=link).save()
    return HttpResponseRedirect(reverse("MyAdminApp:main"))


# Пользователи
@user_passes_test(lambda u: u.is_superuser)
def users(request):
    content = {
        "title": "Пользователи",
        "active_menu": "users",
        "users": User.objects.all().order_by("username")
    }
    return render(request, "MyAdminApp/users.html", content)


@user_passes_test(lambda u: u.is_superuser)
def user_add(request):
    if request.method == "POST":
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            if "mainFormSave" in request.POST:
                user = User.objects.order_by('-pk')[0]
                return HttpResponseRedirect(reverse("myadmin:user_update", args=[user.pk]))
            if "mainFormSaveExit" in request.POST:
                return HttpResponseRedirect(reverse("myadmin:users"))
    else:
        user_form = UserCreateForm()

    content = {
        "title": "Новый пользователь",
        "form_user": user_form,
        "create": True
    }
    return render(request, "MyAdminApp/user.html", content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        user_form.save()
        if "mainFormSave" in request.POST:
            return HttpResponseRedirect(reverse("MyAdminApp:user_update", args=[user.pk]))
        if "mainFormSaveExit" in request.POST:
            return HttpResponseRedirect(reverse("MyAdminApp:users"))
    else:
        user_form = UserUpdateForm(instance=user)
    content = {
        "title": f"Пользователь: {user.username}",
        "form_user": user_form,
        "create": False
    }
    return render(request, "MyAdminApp/user.html", content)


# Бойцы
@login_required()
def fighters(request):
    search = request.GET.get("search", "")

    if search:
        fighters = Fighters.objects.filter(Q(last_name__icontains=search) |
                                           Q(nickname__icontains=search) |
                                           Q(first_name__icontains=search))
    else:
        fighters = Fighters.objects.all()

    title = "Бойцы"
    content = {
        "title": title,
        "active_menu": "fighters",
        "fighters": fighters,
    }
    return render(request, "MyAdminApp/fighters.html", content)


@login_required()
def fighter_add(request):
    if request.method == "POST":
        form = FighterForm(request.POST, request.FILES)
        if form.is_valid():
            if "mainFormSave" in request.POST:
                fighter = Fighters(
                    last_name=request.POST["last_name"],
                    first_name=request.POST["first_name"],
                    nickname=request.POST["nickname"],
                    photo=request.FILES["photo"],
                    instagram=request.POST["instagram"],
                    country=request.POST["country"],
                    date_birth=request.POST["date_birth"],
                    height=request.POST["height"],
                    weight=request.POST["weight"],
                    weight_category=WeightCategories.objects.get(pk=int(request.POST["weight_category"])),
                    span_of_hands=request.POST["span_of_hands"],
                    rack=request.POST["rack"],
                    team=Clubs.objects.get(pk=int(request.POST["team"])),
                    sports=Sports.objects.get(pk=int(request.POST["sports"])),
                    contract=request.POST["contract"],
                )
                fighter.save()
                return HttpResponseRedirect(reverse("myadmin:fighter_update", args=[fighter.pk]))
            if "mainFormSaveExit" in request.POST:
                form.save()
                return HttpResponseRedirect(reverse("myadmin:fighters"))
    else:
        content = {
            "media_url": settings.MEDIA_URL,
            "fighter": Fighters,
            "form_fighter": FighterForm
        }
        return render(request, "MyAdminApp/fighter.html", content)


@login_required()
def fighter_update(request, pk):
    fighter = get_object_or_404(Fighters, pk=pk)
    if request.method == "POST":
        form = FighterForm(request.POST, request.FILES, instance=fighter)
        if form.is_valid():
            if "mainFormSave" in request.POST:
                form.save()
                return HttpResponseRedirect(reverse("MyAdminApp:fighter_update", args=[fighter.pk]))
            if "mainFormSaveExit" in request.POST:
                form.save()
                return HttpResponseRedirect(reverse("MyAdminApp:fighters"))
    else:
        form = FighterForm(instance=fighter)
    content = {
        "media_url": settings.MEDIA_URL,
        "fighter": fighter,
        "form_fighter": form,
    }
    return render(request, "MyAdminApp/fighter.html", content)


# Дополнительно
@login_required()
def others(request):
    content = common.get_content_others()
    return render(request, "MyAdminApp/others.html", content)


@login_required()
def object_add(request):
    """
    Вызывается с адресов:
    path("others/sports/add/", adminapp.object_add, name="sport_add"),
    path("others/promo/add/", adminapp.object_add, name="promotions_add"),
    path("others/clubs/add/", adminapp.object_add, name="clubs_add"),

    не повторяет код, если меняется path необходимо поменять переменную forms
    :param request:
    :return:
    """
    forms = dict(sports=SportsForm, promo=PromotionsForm, clubs=ClubsForm)

    form_name = None
    for key, value in forms.items():
        if key in request.path:
            form_name = value
            break

    if request.method == "POST" and form_name is not None:
        form = form_name(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse("MyAdminApp:others"))


# TODO: Доделать проверку веса
@login_required()
def wc_add(request):
    if request.method == "POST":
        form = WeightCategoriesForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect(reverse("MyAdminApp:others"))
