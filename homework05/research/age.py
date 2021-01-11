import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends  # type: ignore


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    age = []
    time = dt.date.today()
    friends = get_friends(user_id, fields=["bdate"]).items
    for friend in friends:
        try:
            bdate = dt.datetime.strptime(friend["bdate"], "%d.%m.%Y")  # type: ignore
        except (KeyError, ValueError):
            continue
        age.append(
            time.year
            - bdate.year
            - (time.month < bdate.month or (time.month == bdate.month and time.day < bdate.day))
        )

    if age:
        return statistics.median(age)
    return None
