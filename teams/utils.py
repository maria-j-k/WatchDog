from datetime import date, timedelta


def compute_age(birth):
    now = date.today()
    if  birth.month == now.month:
        years = now.year - birth.year
    else:
        years = now.year - birth.year - ((birth.month, birth.day) > (now.month, now.day))
    months = now.month - birth.month if now.month >= birth.month else 12 -(birth.month -now.month)
    days = now.day - birth.day
    if days < -15:
        if months == 0:
            years -= 1
            months = 11
        else:
            months -= 1
    elif days > 15:
        if months == 11:
            years += 1
            months = 0
        else:
            months += 1
    age = {
        'years': years,
        'months': months
        }
    return age

