from card_creator import Card_creator
from card_creator_config import Card_creator_config
from card_utils import card_from_types
from dev_tasks import parse_tasks_file
from kaiten.card import CardType
from kaiten.session import Session

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

def create_cards(session: Session, path: str, config: Card_creator_config, find_bugs: bool = False,
          find_features: bool = False) -> None:
    if find_bugs:
        create_cards_from_text_file_bugs(path=path, config=config, session=session)
    if find_features:
        create_cards_from_text_file_features(path=path, config=config, session=session)


def output_planned_tasks(path: str) -> None:
    for task in parse_tasks_file(path):
        print(task)