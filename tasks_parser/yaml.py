try:
    from yaml import safe_load
except ImportError:
    raise ImportError('You cannot work with the YAML format because you do not '
                      'have the corresponding package installed on your system.')

from kaiten.session import Session
from kaiten.user import User
from utils.card_utils import card_from_id, card_from_types
from kaiten.card import CardType
from utils.card_creator import Card_creator
from utils.card_creator_config import Card_creator_config

def create_cards(session: Session, path: str, def_config_name: str, user: User = None) -> None:
    if user is None:
        user = User(session)

    with open(path) as f:
        parents = safe_load(f)

    if parents is None:
        print("Parsing YAML failed.")
    for parent in parents:
        if 'ggis_id' not in parent and 'id' not in parent:
            print("Вы не задали ни `ggis_is` ни `id` для родительской карточки. Она будет пропущена.")
            continue
        if 'tasks' not in parent:
            print("Для карточки не обнаружено ни одной задачи (поле `tasks`) - пропущено")
            continue
        if len(parent['tasks']) == 0:
            print("Для карточки не обнаружено ни одной задачи (поле `tasks`) - пропущено")
            continue
        types = set[CardType]()
        if 'type' in parent:
            type_upper = parent['type'].upper()
            if type_upper == 'US-EN':
                types.add(CardType.User_story)
                types.add(CardType.Enabler)
            elif type_upper == 'EN':
                types.add(CardType.Enabler)
            elif type_upper == 'BUG':
                types.add(CardType.Bug)
            elif type_upper == 'DB':
                types.add(CardType.Techdolg)
        parent_card = None
        find_by_ggis_id = False
        if 'id' in parent:
            try:
                int_id = int(parent['id'])
            except ValueError:
                int_id = None
            if int_id is not None:
                parent_card = card_from_id(session=session, identificator=int_id)
        if parent_card is None and 'ggis_id' in parent:
            parent_card = card_from_types(session=session, type_ids=types, identificator=parent['ggis_id'],
                                          try_convert_ident_to_id=False)
            find_by_ggis_id = True
        if parent_card is None:
            print(f'Не удалось найти родителя с конфигурацией {parent} - пропущено')
            continue
        if not find_by_ggis_id:
            if len(types) > 0:
                if parent_card.card_type not in types:
                    parent_card_str = str(parent)
                    if hasattr(parent_card, 'title'):
                        parent_card_str = parent_card.title
                    print(f'Карточка `{parent_card_str}` не соответствует указанному типу {parent['type']} - пропущено')
                    continue
        for task in parent['tasks']:
            if 'name' not in task:
                print('Не задано имя таски! Пропускаем')
                continue
            config = def_config_name
            size = None
            if 'config' in task:
                config = task["config"]
            if 'size' in task:
                size = task["size"]
            Card_creator(task["name"], Card_creator_config(config, user, size), parent_card, session)


def output_planned_tasks(path: str) -> None:
    with open(path) as f:
        parents = safe_load(f)
    try:
        for parent in parents:
            card_type = "ALL"
            if 'type' in parent:
                card_type = parent['type']
            parent_str = ""
            if 'ggis_id' in parent:
                parent_str = str(parent['ggis_id'])
            if 'id' in parent:
                if len(parent_str) > 0:
                    parent_str = f'{parent_str}(#{parent["id"]})'
                else:
                    parent_str = f'#{parent["id"]}'
            for task in parent['tasks']:
                if "config" not in task:
                    task["config"] = "по-умолчанию"
                if "size" not in task:
                    task["size"] = "по умолчанию из кофигурации"
                print(
                    f"{card_type} {parent_str} '{task['name']}' с кофигурацей {task['config']} cо временем {task['size']}")
    except KeyError:
        print("Неверный формат yaml-файла!")
        exit(1)