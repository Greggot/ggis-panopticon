#!/bin/python3

import json
import sys
import argparse
from tui.MainScreen import start_interactive as run_tui
from kaiten.session_manager import get_session
from kaiten.session import Session
from kaiten.user import User
from utils.card_creator_config import Card_creator_config
from utils.config_utils import check_and_prepare_configs_path
from tasks_parser.simple import create_cards_from_text_file_bugs, create_cards_from_text_file_features, \
    output_planned_tasks

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=sys.argv[0], description='Скрипт для автоматизированного создания задач')
    parser.add_argument('--tui', help='перейти в интерактивный режим', action='store_true')
    args = parser.parse_args()
    is_interactive = args.tui

    if is_interactive :
        run_tui('data/tasks.txt')
        exit(0)

    check_and_prepare_configs_path()
    config_name = 'delivery'
    (user, session) = get_session('env/env.json')

    print('Пользователь: ', user)

    # output_column('Бэклог спринта')
    # output_column('В работе')
    # output_column('Ревью')
    # output_column('Тестирование')
    # output_column('Готово')

    # output_stories_enablers(session)

    # Кое-кто понадвигал карточки и поубирал стори, не буду
    # показывать пальцем. В общем, этот список сейчас смотреть
    # нет смысла
    # print('Карточки без родителей: {')
    # for card in user.parentless_cards():
    #     print('  ', card)
    # print('}')

    output_planned_tasks('data/tasks.txt')
    print(f'Создать карточки с конфигом {config_name}? [Y/N]:\n')

    agreement = input()
    if agreement.upper()[0] == 'Y':
        config = Card_creator_config(config_name, user)
        # create_cards_from_text_file_bugs(session=session, path='data/tasks.txt', config=config)
        create_cards_from_text_file_features(session=session, path='data/tasks.txt', config=config)