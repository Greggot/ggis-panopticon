#!/bin/python3

import json
from kaiten.session import Session
from kaiten.user import User
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
    check_and_prepare_configs_path()
    config_name = 'delivery'
    env = json.load(open('env/env.json'))

    session = Session(server=env['kaiten_host'], token=env['kaiten_token'])
    user = User(session)
    print('Пользователь: ', user)

    # output_column('Бэклог спринта')
    # output_column('В работе')
    # output_column('Ревью')
    # output_column('Тестирование')
    # output_column('Готово')

    # output_stories_enablers(session)

    print('Карточки без родителей: {')
    for card in user.parentless_cards():
        print('  ', card)
    print('}')

    output_planned_tasks(parse_tasks_file('data/tasks.txt'))
    print(f'Создать карточки с конфигом {config_name}? [Y/N]:\n')

    agreement = input()
    if agreement.upper()[0] == 'Y':
        config = Card_creator_config(config_name, user)
        # create_cards_from_text_file_bugs('data/tasks.txt', config)
        create_cards_from_text_file_features('data/tasks.txt', config)