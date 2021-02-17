from MainApp.models import *
from MyAdminApp.forms import *
import re

def get_content_others():
    return {
        "title": "Дополнительно",
        "active_menu": "others",
        "sports": Sports.objects.all(),
        "promotions": Promotions.objects.all(),
        "clubs": Clubs.objects.all(),
        "weight_categories": WeightCategories.objects.all(),
        'form_sports': SportsForm(),
        'form_promotions': PromotionsForm(),
        'form_podcasts': PodcastsForm(),
        'form_weight_categories': WeightCategoriesForm(),
        'form_clubs': ClubsForm(),
    }

def get_info_podcast(HTML_code):
    if not HTML_code:
        return "", "", ""
    pattern_src = r"(https:\/\/music.yandex.ru\/iframe\/#track\/[0-9]+\/[0-9]+)"
    pattern_href = r"(https:\/\/music.yandex.ru\/album\/[0-9]+\/track\/[0-9]+)"
    pattern_desc = r"(>[?!,.()A-z-а-яА-ЯёЁ0-9\s]+<\/a>)"

    result_src = re.findall(pattern_src, HTML_code)
    result_href = re.findall(pattern_href, HTML_code)
    result_desc = re.findall(pattern_desc, HTML_code)

    src = result_src[0] if result_src else ""
    href = result_href[0] if result_href else ""
    desc = str(result_desc[0]).replace("</a>", "").replace(">", "") if result_desc else ""
    return src, href, desc
