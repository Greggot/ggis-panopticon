import requests
from card import Card, CardType
from kaiten.session import Session
from typing import List, Iterable, Set
from user import User
from dev_tasks import Dev_tasks

def cards_type_request(session: Session, type_id: int, offset: int = 0, limit: int = 100, query: str = None):
    params = {
        "type_ids": type_id,
        "condition": 1,
        "offset": offset,
        "limit": limit,
    }
    if query is not None:
        params["query"] = query
    request = requests.get(session.cards_url, headers=session.headers, params=params)
    return request.json()


def cards_of_type(session: Session, type_id: int, offset: int = 0) -> list:
    full_list = []
    temp_list = cards_type_request(session, type_id, offset)
    while len(temp_list) == 100:
        offset += 100
        full_list += temp_list
        temp_list = cards_type_request(session, type_id, offset)
    full_list += temp_list
    return full_list

def tag_from_card_type(type: CardType) -> str:
    if type == CardType.Feature:
        return ':F'
    if type == CardType.User_story:
        return ':US'
    if type == CardType.Bug:
        return ':BUG'
    if type == CardType.Enabler:
        return ':EN'


def card_from_type(session: Session, type_id: CardType, identificator: str) -> Card | None:
    tag = tag_from_card_type(type_id)
    card_ident = f"{tag}.{identificator}."
    single_list = cards_type_request(session=session, type_id=type_id.value, limit=1, query=card_ident)
    if len(single_list) == 1:
        card = Card(single_list[0])
        if card.title.find(tag, 0) >= 0:
            card.ggis_id_from_title(tag)
            return card
    return None


def card_from_types(session: Session, type_ids: Set[CardType], identificator: str) -> Card | None:
    for type_id in type_ids:
        card = card_from_type(session=session, type_id=type_id, identificator=identificator)
        if card is not None:
            return card

    return None


def cards_of_ggis_id(session: Session, type_id: CardType, id_tag: str) -> Iterable[Card]:
    card_list = []
    full_list = cards_of_type(session, type_id.value)
    for member in full_list:
        card = Card(member)
        if card.title.find(id_tag, 0) >= 0:
            card.ggis_id_from_title(id_tag)
            card_list.append(card)
    card_list.sort(key=lambda card: card.id)
    print('Finished search of ', id_tag)
    return card_list


def features(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, CardType.Feature, ':F')


def user_stories(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, CardType.User_story, ':US')


def enablers(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, CardType.Enabler, ':EN')


def bugs(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, CardType.Bug, ':BUG')


def output_column(user: User, title: str) -> None:
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


def output_planned_tasks(dev_task_list: List[Dev_tasks]) -> None:
    for task in dev_task_list:
        print(task)