#!/bin/python3

from click import confirm
from kaiten.session_manager import get_session
from tui.MainScreen import start_interactive as run_tui
from utils.card_creator_config import Card_creator_config
from utils.config_utils import check_and_prepare_configs_path
import os.path

from tasks_parser.simple import create_cards as create_cards_simple, output_planned_tasks as output_planned_tasks_simple
from tasks_parser.json import create_cards as create_cards_json, output_planned_tasks as output_planned_tasks_json
from tasks_parser.yaml import create_cards as create_cards_yaml, output_planned_tasks as output_planned_tasks_yaml

def output_planned_tasks(path: str) -> None:
    split_filename = os.path.splitext(path)
    if len(split_filename) >= 2:
        if split_filename[1] == '.json':
            output_planned_tasks_json(path)
        elif split_filename[1] == '.yaml':
            output_planned_tasks_yaml(path)
        else:
            output_planned_tasks_simple(path)

def skird(config_name: str = 'delivery', tasks_file: str = 'data/tasks.txt', find_bugs: bool = False,
          find_features: bool = False, show_parentless: bool = False):
    if not os.path.isfile(tasks_file):
        print(f"Не найден файл конфигурации с тасками ({tasks_file})")
        exit(1)

    (user, session) = get_session('env/env.json')
    print('Пользователь: ', user)

    if show_parentless:
        print('Карточки без родителей: {')
        for card in user.parentless_cards():
            print('  ', card)
        print('}')

    output_planned_tasks(tasks_file)

    if confirm(f'Создать карточки с конфигом {config_name} по-умолчанию?', default=True):
        split_filename = os.path.splitext(tasks_file)
        if len(split_filename) >= 2:
            if split_filename[1] == '.json':
                create_cards_json(path=tasks_file, def_config_name=config_name, session=session, user=user)
                return
            elif split_filename[1] == '.yaml':
                create_cards_yaml(path=tasks_file, def_config_name=config_name, session=session, user=user)
                return
        config = Card_creator_config(config_name, user)
        create_cards_simple(session=session, path=tasks_file, config=config, find_bugs=find_bugs, find_features=find_features)


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
    parser.add_argument('--tui', help='перейти в интерактивный режим', action='store_true')
    parser.add_argument('-p', '--path', nargs='?', help='путь до файла с прописанными задачами',
                        default=tasks_file)
    parser.add_argument('-b', '--bugs', action='store_true', help="искать баги (игнорируется с json-форматом)")
    parser.add_argument('--no-features', action='store_false', help="не искать фичи (игнорируется с json-форматом)")
    parser.add_argument('--parentless', action='store_true', help="вывести список карточек без родителей")

    args = parser.parse_args()
    skird_args = {
        "tasks_file"      : args.path,
        "config_name"     : args.type, 
        "find_bugs"       : args.bugs, 
        "find_features"   : args.no_features,
        "show_parentless" : args.parentless
    } 

    is_interactive = args.tui
    if is_interactive :
        run_tui(skird_args.path)
        exit(0)

    skird(**skird_args)
