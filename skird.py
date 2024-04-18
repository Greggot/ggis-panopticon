#!/bin/python3

from kaiten.session import Session
import json

from user import User
from card import user_stories, enablers, bugs, features
from dev_tasks import parse_tasks_file
from input_task import Input_task
from input_config import Input_config
import os.path


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
    use_json = False
    split_filename = os.path.splitext(path)
    if len(split_filename) >= 2:
        if split_filename[1] == '.json':
            use_json = True
    if not use_json:
        for task in parse_tasks_file(path):
            print(task)
    else:
        with open(path) as f:
            json_tasks = json.load(f)
        try:
            for type in json_tasks:
                for parent in json_tasks[type]:
                    for task in json_tasks[type][parent]:
                        if "config" not in task:
                            task["config"] = "по-умолчанию"
                        if "size" not in task:
                            task["size"] = "по умолчанию из кофигурации"
                        print(f"{type} {parent} '{task['name']}' с кофигурацей {task['config']} cо временем {task['size']}")
        except KeyError:
            print("Неверный формат json-файла!")
            exit(1)


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


def json_parsing_parent(parent_list, json_tasks_group, def_config_name: str):
    for parent in parent_list:
        for dev_tasks_parent in json_tasks_group:
            if parent.ggis_id != dev_tasks_parent.strip():
                continue
            if parent.is_late:
                print(f'[WARNING] Истек срок карточки: {parent.title}, deadline: {parent.deadline}')
            for task in json_tasks_group[dev_tasks_parent]:
                config = def_config_name
                size = None
                if "config" in task:
                    config = task["config"]
                if "size" in task:
                    size = task["size"]
                Input_task(task["name"], Input_config(config, user), parent, session, size)


def create_cards_from_json(path: str, def_config_name: str) -> None:
    with open(path) as f:
        json_tasks = json.load(f)
    try:
        if "US-EN" in json_tasks:
            if len(json_tasks["US-EN"]) > 0:
                json_parsing_parent(user_stories(session) + enablers(session), json_tasks["US-EN"], def_config_name)
        if "BUG" in json_tasks:
            if len(json_tasks["BUG"]) > 0:
                json_parsing_parent(bugs(session), json_tasks["BUG"], def_config_name)
    except KeyError:
        print("Неверный формат json-файла!")
        exit(1)


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
                        help='выбор типа создаваемых тасков по-умолчанию', choices=['delivery', 'discovery'],
                        default=config_name)
    parser.add_argument('-p', '--path', nargs='?', help='путь до файла с прописанными задачами',
                        default=tasks_file)
    parser.add_argument('-b', '--bugs', action='store_true', help="искать баги (игнорируется с json-форматом)")
    parser.add_argument('--no-features', action='store_false', help="не искать фичи (игнорируется с json-форматом)")

    args = parser.parse_args()
    find_bugs = args.bugs
    find_features = args.no_features
    config_name = args.type
    tasks_file = args.path

    if not os.path.isfile(tasks_file):
        print(f"Не найден файл конфигурации с тасками ({tasks_file})")
        exit(1)

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

    use_json = False
    split_filename = os.path.splitext(tasks_file)
    if len(split_filename) >= 2:
        if split_filename[1] == '.json':
            use_json = True

    output_planned_tasks(tasks_file)
    if click.confirm(f'Создать карточки с конфигом {config_name} по-умолчанию?', default=True):
        if not use_json:
            config = Input_config(config_name, user)
            if find_bugs:
                create_cards_from_text_file_bugs(tasks_file, config)
            if find_features:
                create_cards_from_text_file_features(tasks_file, config)
        else:
            create_cards_from_json(tasks_file, config_name)
