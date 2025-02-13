import requests
import asyncio
from requests import Response
from kaiten.card import Card, CardType
from kaiten.session import Session
from typing import List, Iterable, Set
from kaiten.user import User
from dev_tasks import Dev_tasks

""" type_id - тип карточек (сторя, энейблер...)
    offset - сдвиг, если требуется запросить >100 карточек
    limit - максимальное количество карточек для получения
    query - текстовый запрос для поиска в названии карточки
""" 
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

def card_id_request(session: Session, type_id: int) -> Response:
    request = requests.get(session.card_url(type_id), headers=session.headers)
    return request


""" API Кайтена возвращает по 100 карточек максимум за раз. Для обхода ограничения 
    используется поле 'offset' в запросе. С ним были какие-то проблемы, мы так и не выяснили.
    Он мог пропускать какие-то карточки
""" 
def cards_of_type(session: Session, type_id: int, offset: int = 0) -> list:
    full_list = []
    temp_list = cards_type_request(session, type_id, offset)
    while len(temp_list) == 100:
        offset += 100
        full_list += temp_list
        temp_list = cards_type_request(session, type_id, offset)
    full_list += temp_list
    return full_list

def identificator_is_id(ident: str) -> int | None:
    if ident.find('.') != -1:
        return None
    try:
        real_id = int(ident)
        if real_id > 10000:
            return real_id
    except ValueError:
        return None
    return None

def card_from_id(session: Session, identificator: int) -> Card | None:
    res = card_id_request(session, identificator)
    if res.status_code != 200:
        return None
    return Card(res.json())

def card_from_id_str(session: Session, identificator: str) -> Card | None:
    real_id = identificator_is_id(identificator)
    if real_id is not None:
        return card_from_id(session, real_id)
    return None

def card_from_type(session: Session, type_id: CardType, identificator: str, try_convert_ident_to_id: bool = False) -> Card | None:
    tag = type_id.tag
    if try_convert_ident_to_id:
        card = card_from_id_str(session, identificator)
        if card is not None:
            if card.title.find(tag, 0) >= 0:
                card.ggis_id_from_title(tag)
                return card
    card_ident = f"{tag}.{identificator}."
    single_list = cards_type_request(session=session, type_id=type_id.value, limit=1, query=card_ident)
    if len(single_list) == 1:
        card = Card(single_list[0])
        if card.title.find(tag, 0) >= 0:
            card.ggis_id_from_title(tag)
            return card
    return None


def card_from_types(session: Session, type_ids: Set[CardType], identificator: str, try_convert_ident_to_id: bool = False) -> Card | None:
    for type_id in type_ids:
        card = card_from_type(session=session, type_id=type_id, identificator=identificator, try_convert_ident_to_id=try_convert_ident_to_id)
        if card is not None:
            return card

    return None

""" Отсортированный список карточек определенного типа, с подходящим ggis_id"""
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
    return cards_of_ggis_id(session, CardType.Feature, CardType.Feature.tag)


def user_stories(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, CardType.User_story, CardType.User_story.tag)


def enablers(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, CardType.Enabler, CardType.Enabler.tag)


def techdolg(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, CardType.Techdolg, CardType.Techdolg.tag)


def bugs(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, CardType.Bug, CardType.Bug.tag)


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

    print('\nTechdolg: ')
    for card in techdolg(client):
        print('  ', card)

async def gather_all_cards(session: Session, offset):
    return requests.get(session.cards_url, headers=session.headers, params={
        "offset": offset
    })

""" Когда-то Рома писал это, чтобы поулчить список карточек тега 'Эс++' 
    Вроде, это можно поправить средствами самого Кайтена, но я пока оставлю
"""
async def es_plus_plus_cards(session: Session) -> Iterable[Card]:
    tasks = []
    for i in range(0, 2000, 100):
        tasks.append(asyncio.create_task(gather_all_cards(session, i)))
    responses = await asyncio.gather(*tasks)
    res = []
    for response in responses:
        for card in (Card(member) for member in response.json()):
            for tag_description in card.__dict__.get('tags', {}):
                if ('name', 'С++') in tag_description.items():
                    res.append(card)
    return res