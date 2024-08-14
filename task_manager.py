#!/bin/python3

import json
import sys
import argparse
import click
import os

from config_utils import check_and_prepare_configs_path

check_and_prepare_configs_path()

parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description='Скрипт для формирования пула задач в виде json-файла')

parser.add_argument('-c', '--clear', help='очистить json перед добавлением', action="store_true")

args = parser.parse_args()


def selectNum(maximum: int, text: str, default: int = None):
    while True:
        selected = click.prompt(text, type=int, default=default)
        if selected == 0:
            print("Пока!")
            exit(0)
        if 1 <= selected <= maximum:
            break
        else:
            print(f"Error: '{selected}', is not a valid variant.")
    return selected


tasks_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'tasks.json'))

if args.clear:
    os.remove(tasks_file)
else:
    if os.path.isfile(tasks_file):
        if click.confirm('Очистить предыдущую конфигурацию?', default=False):
            os.remove(tasks_file)

json_data = dict()
if os.path.isfile(tasks_file):
    with open(tasks_file, 'r') as f:
        json_data = json.load(f)

while True:
    card_type = None
    card_parent = None
    if len(json_data) != 0:
        index = 0
        for type in json_data:
            for parent in json_data[type]:
                index += 1
                print(index, type, parent)
        print(index + 1, "новый родитель")
        print(0, "выйти из программы")
        user_select = selectNum(index + 1, "Выберите родителя вашей карточки", index + 1)
        if user_select <= index:
            index = 0
            for type in json_data:
                for parent in json_data[type]:
                    index += 1
                    if index == user_select:
                        card_type = type
                        card_parent = parent
                        break
                if card_parent is not None:
                    break

    if card_type is None:
        card_types = ["ALL", "US-EN", "BUG", "US", "EN"]
        print("1. Любой тип (мне лень вспоминать)")
        print("2. US или EN")
        print("3. BUG")
        print("4. US")
        print("5. EN")
        print("0. Выйти")
        user_select = selectNum(maximum=5, text="Выберите тип родителя для вашей задачи", default=1)
        card_type = card_types[user_select - 1]
        print(f"Окей, будем создавать карточку для {card_type}")

    if card_parent is None:
        while True:
            try:
                card_parent = click.prompt("Введите идентификатор карточки родителя (к примеру, 81.23468 или 49.9)",
                                           type=str)
                if not card_parent.isspace():
                    break
            except UnicodeDecodeError:
                print("Что-то пошло не так... Давайте еще раз")

    card_name = None
    while True:
        try:
            card_name = click.prompt("Введите название вашей задачи", type=str)
            if not card_name.isspace():
                break
        except UnicodeDecodeError:
            print("Что-то пошло не так... Давайте еще раз")

    config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'env', 'skird_config'))
    config_files = os.listdir(config_dir)

    index = 0
    for file in config_files:
        index += 1
        print(index, os.path.splitext(file)[0])

    print(0, "выйти из программы")

    user_select = selectNum(index, "Выбирете тип (конфигурацию) создаваемой карточки", 1)
    config_file = config_files[user_select - 1]
    card_config = os.path.splitext(config_file)[0]

    with open(os.path.join(config_dir, config_file), 'r') as f:
        card_size = int(json.load(f)["size_text"].split()[0])

    card_size = click.prompt("Введите размер карточки в часах", type=int, default=card_size)

    if card_type not in json_data:
        json_data[card_type] = {}

    if card_parent not in json_data[card_type]:
        json_data[card_type][card_parent] = []

    new_card = {
        "name": card_name,
        "config": card_config,
        "size": card_size
    }

    json_data[card_type][card_parent].append(new_card)

    if not os.path.exists(os.path.abspath(os.path.join(tasks_file, os.pardir))):
        os.mkdir(os.path.abspath(os.path.join(tasks_file, os.pardir)))

    with open(tasks_file, "w", encoding="utf-8") as write:
        json.dump(json_data, write, sort_keys=True, indent=2, ensure_ascii=False)

    if not click.confirm('Добавить еще карточку?', default=False):
        break

if click.confirm('Запустить скрипт создания новых карточек с Вашей конфигурацией?', default=True):
    import skird_cmd

    skird_cmd.skird(tasks_file=tasks_file)
