
from kaiten.session import Session
from datetime import timedelta, datetime

import requests

weekend_days = [5, 6]
"""!Номера дней недели для субботы и воскресенья"""

class Time_log_input():
    """!Входные настройки для автоматического списания времени"""

    def __init__(self, time_log_json):
        self.__data__ = time_log_json
        for key in time_log_json:
            setattr(self, key, time_log_json[key])

    def date_range(self):
        """!Список дат, в течение которых требуется списать время. 
            Из списка исключаются выходные дни.
        """
        actual_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        for n in range(self.days_count):
            element_date = actual_date + timedelta(n)
            if element_date.weekday() not in weekend_days:
                yield element_date

    def register_time(self, session: Session):
        """!Списать время в указанную карточку для self.time_spent дней
            по self.time_spent минут.
        """
        for workday in self.date_range():
            requests.post(session.time_logs_url(self.card_id), headers=session.headers, json={
                "role_id": self.role_id,
                "time_spent": self.time_spent,
                "for_date": workday.strftime("%Y-%m-%d")
            })

    @property 
    def what_im_gonna_do(self) -> str:
        return f'Списать по {self.time_spent} минут с {self.start_date} числа в течение {self.days_count} рабочих дней'