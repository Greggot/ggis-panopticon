from kaiten.session import Session
import json

from user import User
from card import user_stories, enablers, bugs, features
from us_tasks import parse_tasks_file
from input_task import Input_task

def output_column(title: str) -> None:
    print()
    print('Карточки ' + title + ': ')
    card_list = user.column_card_list(title)
    card_list.sort(key=lambda card: card.id)
    for card in card_list:
        print('  ' + str(card))
    # print(card_list[0].raw)

def output_stories_enablers(client):
    print()
    print('User stories: ')
    for card in user_stories(client):
        print('  ' + str(card))
    
    print()
    print('Enablers: ')
    for card in enablers(client):
        print('  ' + str(card))

    print()
    print('Features: ')
    for card in features(client):
        print('  ' + str(card))

    print()
    print('Bugs: ')
    for card in bugs(client):
        print('  ' + str(card))

if __name__ == "__main__":
    env_file = open('env/env.json')
    env = json.load(env_file)

    session = Session(server = env['kaiten_host'], token = env['kaiten_token'])
    user = User(session)
    print('Пользователь: ' + str(user))

    output_column('Бэклог спринта')
    output_column('В работе')
    output_column('Ревью')
    output_column('Тестирование')
    output_column('Готово')

    print('Карточки без родителей: ')
    for card in  user.parentless_cards():
        print(card)

    output_stories_enablers(client)

    user_stories = user_stories(client)
    enablers = enablers(client)

    planned_tasks = parse_tasks_file('data/tasks.txt')
    for story in user_stories:
        for tasklist in planned_tasks:
            if story.ggis_id.find(tasklist.story) >= 0:
                for task in tasklist.tasks:
                    input_task = Input_task(task, user, story, client)

    for enabler in enablers:
        for tasklist in planned_tasks:
            if enabler.ggis_id.find(tasklist.story) >= 0:
                for task in tasklist.tasks:
                    input_task = Input_task(task, user, enabler, client)
