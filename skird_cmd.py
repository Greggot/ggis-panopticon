#!/bin/python3
from typing import Set

from kaiten.card import CardType
from card_utils import card_from_types
from kaiten.session import Session
import json

from kaiten.user import User
from dev_tasks import parse_tasks_file
from card_creator import Card_creator
from card_creator_config import Card_creator_config
from config_utils import check_and_prepare_configs_path
import os.path


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
                        print(
                            f"{type} {parent} '{task['name']}' с кофигурацей {task['config']} cо временем {task['size']}")
        except KeyError:
            print("Неверный формат json-файла!")
            exit(1)


def create_cards_from_text_file_features(session: Session, path: str, config: Card_creator_config) -> None:
    for tasklist in parse_tasks_file(path):
        story = card_from_types(session=session, type_ids={CardType.User_story, CardType.Enabler, CardType.Techdolg}, identificator=tasklist.story)
        if story is None:
            print(f'[WARNING] Не удалось отыскать карточку с номером {tasklist.story}')
            continue
        if story.is_late:
            print(f'[WARNING] Истек срок карточки: {story.title}, deadline: {story.deadline}')
        for task in tasklist.tasks:
            Card_creator(task, config, story, session)


def create_cards_from_text_file_bugs(session: Session, path: str, config: Card_creator_config) -> None:
    for tasklist in parse_tasks_file(path):
        bug = card_from_types(session=session, type_ids={CardType.Bug}, identificator=tasklist.story)
        if bug is None:
            print(f'[WARNING] Не удалось отыскать карточку с номером {tasklist.story}')
            continue
        if bug.is_late:
            print(f'[WARNING] Истек срок карточки: {bug.title}, deadline: {bug.deadline}')
        for task in tasklist.tasks:
            Card_creator(task, config, bug, session)


def json_parsing_parents(session: Session, types: Set[CardType], json_tasks_group, def_config_name: str,
                         user: User = None):
    if user is None:
        user = User(session)

    for parent_id in json_tasks_group:
        parent_card = card_from_types(session=session, type_ids=types, identificator=parent_id)
        if parent_card is None:
            print(f'[WARNING] Не удалось отыскать карточку с номером {parent_id}')
            continue
        if parent_card.is_late:
            print(f'[WARNING] Истек срок карточки: {parent_card.title}, deadline: {parent_card.deadline}')
        for task in json_tasks_group[parent_id]:
            config = def_config_name
            size = None
            if "config" in task:
                config = task["config"]
            if "size" in task:
                size = task["size"]
            Card_creator(task["name"], Card_creator_config(config, user, size), parent_card, session)


def create_cards_from_json(session: Session, path: str, def_config_name: str, user: User = None) -> None:
    if user is None:
        user = User(session)

    with open(path) as f:
        json_tasks = json.load(f)
    try:
        if "ALL" in json_tasks:
            if len(json_tasks["ALL"]) > 0:
                json_parsing_parents(session=session, user=user,
                                     types={CardType.User_story, CardType.Enabler, CardType.Bug, CardType.Techdolg},
                                     json_tasks_group=json_tasks["ALL"],
                                     def_config_name=def_config_name)
        if "US-EN" in json_tasks:
            if len(json_tasks["US-EN"]) > 0:
                json_parsing_parents(session=session, user=user,
                                     types={CardType.User_story, CardType.Enabler},
                                     json_tasks_group=json_tasks["US-EN"],
                                     def_config_name=def_config_name)
        if "BUG" in json_tasks:
            if len(json_tasks["BUG"]) > 0:
                json_parsing_parents(session=session, user=user,
                                     types={CardType.Bug},
                                     json_tasks_group=json_tasks["BUG"],
                                     def_config_name=def_config_name)
        if "US" in json_tasks:
            if len(json_tasks["US"]) > 0:
                json_parsing_parents(session=session, user=user,
                                     types={CardType.User_story},
                                     json_tasks_group=json_tasks["US"],
                                     def_config_name=def_config_name)
        if "EN" in json_tasks:
            if len(json_tasks["EN"]) > 0:
                json_parsing_parents(session=session, user=user,
                                     types={CardType.Enabler},
                                     json_tasks_group=json_tasks["EN"],
                                     def_config_name=def_config_name)
        if "DB" in json_tasks:
            if len(json_tasks["DB"]) > 0:
                json_parsing_parents(session=session, user=user,
                                     types={CardType.Techdolg},
                                     json_tasks_group=json_tasks["DB"],
                                     def_config_name=def_config_name)
    except KeyError:
        print("Неверный формат json-файла!")
        exit(1)


def skird(config_name: str = 'delivery', tasks_file: str = 'data/tasks.txt', find_bugs: bool = False,
          find_features: bool = False):
    import click
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
            config = Card_creator_config(config_name, user)
            if find_bugs:
                create_cards_from_text_file_bugs(path=tasks_file, config=config, session=session)
            if find_features:
                create_cards_from_text_file_features(path=tasks_file, config=config, session=session)
        else:
            create_cards_from_json(path=tasks_file, def_config_name=config_name, session=session, user=user)


if __name__ == "__main__":
    import sys
    import argparse

    check_and_prepare_configs_path()

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
    skird(tasks_file=args.path, config_name=args.type, find_bugs=args.bugs, find_features=args.no_features)
