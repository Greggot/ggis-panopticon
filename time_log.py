
from kaiten.session import Session
from typing import Iterable

import requests

class Time_log():
    """!Структура, которую Kaiten возвращает при запросе time-log:
        https://developers.kaiten.ru/card-time-logs/get-time-logs#resAttributes
    """
    def __init__(self, time_log_json):
        self.__data__ = time_log_json
        for key in time_log_json:
            setattr(self, key, time_log_json[key])

    @property
    def hours(self) -> int:
        return int(self.time_spent) // 60

    @property
    def minutes(self) -> int:
        return int(self.time_spent)

def time_logs_from_card(card_id: int, session: Session) -> Iterable[Time_log]:
    """!Получить все списания времени в карточку
        @param card_id Идентификатор в Kaiten
    """
    request = requests.get(session.time_logs_url(card_id), headers=session.headers)
    for time_log in (Time_log(member) for member in request.json()):
        yield time_log