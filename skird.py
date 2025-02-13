#!/bin/python3

import json
import sys
import argparse
from tui.MainScreen import start_interactive as run_tui
from kaiten.session_manager import get_session
from card_utils import user_stories, enablers, bugs, output_planned_tasks
from card_creator import Card_creator
from card_creator_config import Card_creator_config
from dev_tasks import parse_tasks_file
from config_utils import check_and_prepare_configs_path

def create_cards_from_text_file_features(path: str, config: Card_creator_config) -> None:
    tasklists = parse_tasks_file(path)
    for story in user_stories(session) + enablers(session):
        for tasklist in tasklists:
            if story.ggis_id != tasklist.story:
                continue
            if story.is_late:
                print(f'[WARNING] Истек срок карточки: {story.title}, deadline: {story.deadline}')
            for task in tasklist.tasks:
                Card_creator(task, config, story, session)


def create_cards_from_text_file_bugs(path: str, config: Card_creator_config) -> None:
    for bug in bugs(session):
        for tasklist in parse_tasks_file(path):
            if bug.ggis_id != tasklist.story:
                continue
            if bug.is_late:
                print(f'[WARNING] Истек срок карточки: {bug.title}, deadline: {bug.deadline}')
            for task in tasklist.tasks:
                Card_creator(task, config, bug, session)


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

    output_planned_tasks(parse_tasks_file('data/tasks.txt'))
    print(f'Создать карточки с конфигом {config_name}? [Y/N]:\n')

    agreement = input()
    if agreement.upper()[0] == 'Y':
        config = Card_creator_config(config_name, user)
        # create_cards_from_text_file_bugs('data/tasks.txt', config)
        create_cards_from_text_file_features('data/tasks.txt', config)