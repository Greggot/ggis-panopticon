#!/bin/python3

from kaiten.session import Session
import json

from user import User
from card import user_stories, enablers, bugs, features
from us_tasks import parse_tasks_file
from input_task import Input_task
from input_config import Input_config


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
    for story in user_stories(session) + enablers(session):
        for tasklist in parse_tasks_file(path):
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
    import sys
    import argparse
    import click

    config_name = 'delivery'
    tasks_file = 'data/tasks.txt'

    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description='Скрипт для автоматизированного создания задач')
    parser.add_argument('-t', '--type', nargs='?',
                        help='выбор типа создаваемых тасков', choices=['delivery', 'discovery'],
                        default=config_name)
    parser.add_argument('-p', '--path', nargs='?', help='путь до файла с прописанными задачами',
                        default=tasks_file)
    parser.add_argument('-b', '--bugs', action='store_true', help="искать баги")
    parser.add_argument('--no-features', action='store_false', help="не искать фичи")

    args = parser.parse_args()
    find_bugs = args.bugs
    find_features = args.no_features
    config_name = args.type
    tasks_file = args.path

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

    output_planned_tasks(tasks_file)

    if click.confirm(f'Создать карточки с конфигом {config_name}?', default=True):
        config = Input_config(config_name, user)
        if find_bugs:
            create_cards_from_text_file_bugs('data/tasks.txt', config)
        if find_features:
            create_cards_from_text_file_features(tasks_file, config)
