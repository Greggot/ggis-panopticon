from kaiten.session import Session
import json

from user import User
from card import user_stories, enablers, bugs, features
from us_tasks import parse_tasks_file
from input_task import Input_task

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

def create_cards_from_text_file(path: str) -> None:
    planned_tasks = parse_tasks_file(path)
    for task in planned_tasks:
        print(task)

    for story in user_stories(session) + enablers(session) + bugs(session):
        for tasklist in planned_tasks:
            if story.ggis_id != tasklist.story:
                continue
            for task in tasklist.tasks:
                input_task = Input_task(task, user, story, session)

if __name__ == "__main__":
    env_file = open('env/env.json')
    env = json.load(env_file)

    session = Session(server = env['kaiten_host'], token = env['kaiten_token'])
    user = User(session)
    print('Пользователь: ', user)

    # output_column('Бэклог спринта')
    # output_column('В работе')
    # output_column('Ревью')
    # output_column('Тестирование')
    # output_column('Готово')

    print('Карточки без родителей: {')
    for card in user.parentless_cards():
        print('  ', card)
    print('}')

    output_stories_enablers(session)
    create_cards_from_text_file('data/tasks.txt')
