#!/bin/python3

from kaiten.session import Session
import json

from kaiten.user import User
from kaiten.time_log import time_logs_from_card
from time_log_input import Time_log_input

def check_spent_time(user: User, session: Session):
    overall_minutes = 0
    for card in user.card_list():
        print(' ', card.title)
        for time_log in time_logs_from_card(card.int_id, session):
            print(f'Затраченное время: {time_log.hours} at {time_log.for_date}')
            overall_minutes = overall_minutes + time_log.minutes
    print(f'\nВсего затрачено: {overall_minutes // 60} часов')

if __name__ == "__main__":
    env_file = open('env/env.json')
    env = json.load(env_file)

    session = Session(server = env['kaiten_host'], token = env['kaiten_token'])
    user = User(session)
    print('Пользователь: ', user)

    auto_time_log_file = open('env/auto_time_log.json')
    time_log_input = Time_log_input(json.load(auto_time_log_file))
    print(f'{time_log_input.what_im_gonna_do}? [Y/N]:\n')

    agreement = input()
    if agreement.upper()[0] == 'Y':
        time_log_input.register_time(session)
        print(f'\nУспешно списано! Удачи продуктивно потратить сэкономленные {12 * time_log_input.days_count} секунд своей жизни!')
