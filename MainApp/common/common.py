from MainApp.models import *
from django.db.models import Q

def get_fighters_full_info(fighters):
    fighters_list = []

    for fighter in fighters:
        fighters_list.append(
            {
                "f": fighter,
                "static": get_static_fighter(fighter),
            }
        )
    return tuple(fighters_list)

def get_battles(fighter):
    battles_lst = []
    battles_obj = Fights.objects.filter(Q(fighter1=fighter) | Q(fighter2=fighter)).order_by("-date")

    for btl in battles_obj:
        btl_dic = {
            "opponent": None,
            "result": None,
            "status": True,
            "date": btl.date.strftime("%d.%m.%Y"),
            "promotion": btl.promotion,
            "link": btl.link,
        }

        if btl.fighter1 == fighter:
            btl_dic["opponent"] = btl.fighter2
        if btl.fighter2 == fighter:
            btl_dic["opponent"] = btl.fighter1
        if btl.winner == fighter:
            btl_dic["result"] = "Победа"
        else:
            btl_dic["result"] = "Поражение"
            btl_dic["status"] = False

        battles_lst.append(btl_dic)

    return tuple(battles_lst)

def get_static_fighter(fighter):
    static_fighter = {
        "victory": 0,
        "losing": 0,
    }
    battles_count = Fights.objects.filter(Q(fighter1=fighter) | Q(fighter2=fighter)).count()
    static_fighter["victory"] = Fights.objects.filter(winner=fighter).count()
    static_fighter["losing"] = battles_count - static_fighter["victory"]
    return static_fighter
