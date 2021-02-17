from django.db import models
from datetime import date


class SettingsApps(models.Model):
    banners_is_active = models.BooleanField(verbose_name="Баннеры активны", default=False)


class Promotions(models.Model):
    name = models.CharField(verbose_name="Наименование", unique=True, max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = "Промоушены"

    def __str__(self):
        return self.name


class Podcasts(models.Model):
    name = models.CharField(verbose_name="Наименование", unique=False, max_length=100)
    HTML_code = models.TextField(verbose_name="HTML код", blank=True, max_length=3000)
    date_podcast = models.DateTimeField(verbose_name="Дата подкаста", auto_now=True, null=True)
    src = models.CharField(verbose_name="src", unique=False, max_length=250, blank=True)
    href = models.CharField(verbose_name="href", unique=False, max_length=250, blank=True)
    description = models.CharField(verbose_name="description", unique=False, max_length=250, blank=True)

    class Meta:
        verbose_name = "Подкасты"

    def __str__(self):
        return self.name


class WeightCategories(models.Model):
    name = models.CharField(verbose_name="Наименование", unique=True, max_length=100)
    weight_from = models.PositiveIntegerField(verbose_name="вес от", blank=True)
    weight_up_to = models.PositiveIntegerField(verbose_name="вес до", blank=True)

    class Meta:
        verbose_name = "Весовые категории"

    def __str__(self):
        return self.name


class Clubs(models.Model):
    name = models.CharField(verbose_name="Наименование", unique=True, max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = "Клубы"

    def __str__(self):
        return self.name


class Sports(models.Model):
    name = models.CharField(verbose_name="Наименование", unique=True, max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = "Виды спорта"

    def __str__(self):
        return self.name


class Banner(models.Model):
    image = models.ImageField(verbose_name="Изображение", upload_to="banner_img", blank=True)
    is_active = models.BooleanField(verbose_name="Активен", default=False)
    date_create = models.DateTimeField(verbose_name="Дата добавления", auto_now=True)

    class Meta:
        verbose_name = "Баннер"


class Video(models.Model):
    link = models.CharField(verbose_name="Ссылка", blank=True, unique=False, max_length=2000)
    date_create = models.DateTimeField(verbose_name="Дата добавления", auto_now=True)

    class Meta:
        verbose_name = "Основоное видео"


class Fighters(models.Model):
    RIGHT = 'R'
    LEFT = 'L'

    RACK = (
        (RIGHT, 'Правая'),
        (LEFT, 'Левая'),
    )


    last_name = models.CharField(verbose_name="Фамилия", unique=False, max_length=100)
    first_name = models.CharField(verbose_name="Имя", unique=False, max_length=100)
    nickname = models.CharField(verbose_name="Псевдоним", unique=False, blank=True, max_length=100)
    photo = models.ImageField(verbose_name="Фото", upload_to="photo_fighters", blank=True)
    instagram = models.CharField(verbose_name="Инстаграм", unique=False, blank=True, max_length=500)
    country = models.CharField(verbose_name="Страна", unique=False, blank=True, max_length=100)
    date_birth = models.DateField(verbose_name="Дата рождения", blank=True)
    height = models.PositiveIntegerField(verbose_name="Рост", default=0)
    weight = models.PositiveIntegerField(verbose_name="Вес", default=0)
    weight_category = models.ForeignKey(WeightCategories, on_delete=models.CASCADE, default=None, blank=True, null=True)
    span_of_hands = models.IntegerField(verbose_name="Размах рук", default=0)
    rack = models.CharField(verbose_name="Стойка", max_length=1, choices=RACK, default=LEFT)
    team = models.ForeignKey(Clubs, on_delete=models.CASCADE, default=None, blank=True, null=True)
    sports = models.ForeignKey(Sports, on_delete=models.CASCADE, default=None, blank=True, null=True)
    # participant = models.
    contract = models.CharField(verbose_name="Контракт", unique=False, blank=True, max_length=100)

    class Meta:
        verbose_name = "Бойцы"
        ordering = ["last_name"]

    def __str__(self):
        return f'{self.last_name} "{self.nickname}" {self.first_name}'

    @property
    def get_age(self):
        today = date.today()
        return today.year - self.date_birth.year - ((today.month, today.day) < (self.date_birth.month, self.date_birth.day))

    @property
    def get_first_last_name(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def get_rack(self):
        racks = {self.LEFT: "Левая", self.RIGHT: "Правая", }
        return racks[self.rack]

    # @property
    # def get_participant(self):
    #     return Participant.objects.filter(fighter=self.id).values_list('id', flat=True)


class Participant(models.Model):
    fighter = models.ForeignKey(Fighters, on_delete=models.SET_NULL, null=True)
    promotion = models.ForeignKey(Promotions, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Боец и Промо"


class Fights(models.Model):
    fighter1 = models.ForeignKey(Fighters, on_delete=models.SET_NULL, related_name='fighter1', null=True, default=None)
    fighter2 = models.ForeignKey(Fighters, on_delete=models.SET_NULL, related_name='fighter2', null=True, default=None)
    winner = models.ForeignKey(Fighters, on_delete=models.SET_NULL, related_name='winner', null=True, default=None)
    date = models.DateField(verbose_name="Дата боя", blank=True)
    promotion = models.ForeignKey(Promotions, on_delete=models.SET_NULL, null=True, default=None)
    link = models.CharField(verbose_name="Ссылка", blank=True, unique=False, max_length=2000)

    class Meta:
        verbose_name = "Бои"
