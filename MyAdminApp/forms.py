import datetime

from django.forms import ModelForm
from django import forms
from MainApp.models import *
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class UserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "is_active", "is_superuser")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["is_active"].widget.attrs["class"] = "form-check-input"
        self.fields["is_superuser"].widget.attrs["class"] = "form-check-input"


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "is_active", "is_superuser")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["is_active"].widget.attrs["class"] = "form-check-input"
        self.fields["is_superuser"].widget.attrs["class"] = "form-check-input"


class BannersForm(ModelForm):
    class Meta:
        model = Banner
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].widget.attrs["class"] = "form-control"
        self.fields["is_active"].widget.attrs["class"] = "form-check-input"


class SportsForm(ModelForm):
    class Meta:
        model = Sports
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label


class PromotionsForm(ModelForm):
    class Meta:
        model = Promotions
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label


class PodcastsForm(ModelForm):
    class Meta:
        model = Podcasts
        fields = "__all__"
        # TODO: Добавить поле даты на форму взять пример из формы бойца

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label


class WeightCategoriesForm(ModelForm):
    class Meta:
        model = WeightCategories
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label


class ClubsForm(ModelForm):
    class Meta:
        model = Clubs
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["link"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["link"].widget.attrs["placeholder"] = "Ссылка на YouTube"


class FighterForm(ModelForm, forms.Form):
    age = forms.IntegerField(initial=0)

    class Meta:
        model = Fighters
        fields = "__all__"
        widgets = {
            'date_birth': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control form-control-sm',
                       'placeholder': 'Select a date',
                       'type': 'date',
                       'onchange': "get_age(this.value)",
                       }),
        }

    def __init__(self, *args, **kwargs):
        super(FighterForm, self).__init__(*args, **kwargs)
        self.fields["last_name"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["first_name"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["nickname"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["photo"].widget.attrs["class"] = "form-control"
        self.fields["instagram"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["country"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["date_birth"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["age"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields['age'].widget.attrs['readonly'] = True
        self.fields["height"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["weight"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["weight_category"].widget.attrs["class"] = "form-select form-select-sm"
        self.fields["span_of_hands"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["rack"].widget.attrs["class"] = "form-select form-select-sm"
        self.fields["team"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["sports"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["contract"].widget.attrs["class"] = "form-control form-control-sm"


class BattleForm(ModelForm):
    class Meta:
        model = Fights
        fields = "__all__"
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fighter1"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["fighter2"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["winner"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["date"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["promotion"].widget.attrs["class"] = "form-select form-select-sm"
        self.fields["link"].widget.attrs["class"] = "form-control form-control-sm"
