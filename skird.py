#!/bin/python3

import json
from kaiten.session import Session
from kaiten.user import User
from card_utils import user_stories, enablers, bugs, output_planned_tasks, card_from_id
from card_creator import Card_creator
from card_creator_config import Card_creator_config
from dev_tasks import parse_tasks_file
from config_utils import check_and_prepare_configs_path

def create_card_from_custom_id(tasklist) -> None:
    story = card_from_id(session, tasklist.custom_id)
    if story is None:
        print(f'Cannot find story {tasklist.custom_id}')
        return
    for task in tasklist.tasks:
        Card_creator(task, config, story, session)

def create_cards_from_text_file_features(path: str, config: Card_creator_config) -> None:
    tasklists = parse_tasks_file(path)
    story_enablers = user_stories(session) + enablers(session)

    for tasklist in tasklists:
        if tasklist.custom_id is None:
            for story in story_enablers:
                if story.ggis_id != tasklist.story:
                    continue
                for task in tasklist.tasks:
                    Card_creator(task, config, story, session)
        else:
            create_card_from_custom_id(tasklist)


def create_cards_from_text_file_bugs(path: str, config: Card_creator_config) -> None:
    tasklists = parse_tasks_file(path)
    story_enablers = bugs(session)

    for tasklist in tasklists:
        if tasklist.custom_id is None:
            for story in story_enablers:
                if story.ggis_id != tasklist.story:
                    continue
                for task in tasklist.tasks:
                    Card_creator(task, config, story, session)
        else:
            create_card_from_custom_id(tasklist)



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