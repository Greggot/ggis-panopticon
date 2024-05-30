#!/bin/python3

from kaiten.session import Session
import json

from user import User
from card import user_stories, enablers, bugs, features
from dev_tasks import parse_tasks_file
from input_task import Input_task
from input_config import Input_config
from helper import check_and_prepare_configs_path


def output_column(title: str) -> None:
    print('\n Карточки ' + title + ': ')
    for card in user.column_card_list(title):
        print('  ', card)


def output_stories_enablers(client):
    print('\nUser stories: ')
    for card in user_stories(client):
        print('  ', card)

    print('\nEnablers: ')
    for card in enablers(client):
        print('  ', card)

    print('\nFeatures: ')
    for card in features(client):
        print('  ', card)

    print('\nBugs: ')
    for card in bugs(client):
        print('  ', card)


def output_planned_tasks(path: str) -> None:
    for task in parse_tasks_file(path):
        print(task)


def create_cards_from_text_file_features(path: str, config: Input_config) -> None:
    tasklists = parse_tasks_file(path)
    for story in user_stories(session) + enablers(session):
        for tasklist in tasklists:
            if story.ggis_id != tasklist.story:
                continue
            if story.is_late:
                print(f'[WARNING] Истек срок карточки: {story.title}, deadline: {story.deadline}')
            for task in tasklist.tasks:
                input_task = Input_task(task, config, story, session)


def create_cards_from_text_file_bugs(path: str, config: Input_config) -> None:
    for bug in bugs(session):
        for tasklist in parse_tasks_file(path):
            if bug.ggis_id != tasklist.story:
                continue
            if bug.is_late:
                print(f'[WARNING] Истек срок карточки: {bug.title}, deadline: {bug.deadline}')
            for task in tasklist.tasks:
                input_task = Input_task(task, config, bug, session)


if __name__ == "__main__":
    check_and_prepare_configs_path()

    config_name = 'delivery'
    env_file = open('env/env.json')
    env = json.load(env_file)

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

    output_planned_tasks('data/tasks.txt')
    print(f'Создать карточки с конфигом {config_name}? [Y/N]:\n')

    agreement = input()
    if agreement.upper()[0] == 'Y':
        config = Input_config(config_name, user)
        # create_cards_from_text_file_bugs('data/tasks.txt', config)
        create_cards_from_text_file_features('data/tasks.txt', config)