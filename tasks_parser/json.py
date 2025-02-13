import json
from typing import Set

from utils.card_creator import Card_creator
from utils.card_creator_config import Card_creator_config
from utils.card_utils import card_from_id_str, card_from_types
from kaiten.card import CardType
from kaiten.session import Session
from kaiten.user import User


def json_parsing_parents(session: Session, types: Set[CardType], json_tasks_group, def_config_name: str,
                         user: User = None):
    if user is None:
        user = User(session)

    for parent_id in json_tasks_group:
        if len(types) == 0 or len(types) >= len(CardType):
            parent_card = card_from_id_str(session=session, identificator=parent_id)
            if parent_card is None:
                parent_card = card_from_types(session=session, type_ids=types, identificator=parent_id)
        else:
            parent_card = card_from_types(session=session, type_ids=types, identificator=parent_id,
                                          try_convert_ident_to_id=True)
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


def create_cards(session: Session, path: str, def_config_name: str, user: User = None) -> None:
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


def output_planned_tasks(path: str) -> None:
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