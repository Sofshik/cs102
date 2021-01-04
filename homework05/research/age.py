import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    age = []
    time = dt.date.today()
    friends = get_friends(user_id, fields=["birth"]).items
    for friend in friends:
        try:
            birth = dt.datetime.strptime(friend["birth"], "%d.%m.%Y")  # type: ignore
        except (KeyError, ValueError):
            continue
        ages.append(
            now.year
            - birth.year
            - (now.month < birth.month or (now.month == birth.month and now.day < birth.day))
        )

    if ages:
        return statistics.median(ages)
    return None