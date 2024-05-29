import requests
import json
import dateutil
import dateutil.parser
from datetime import date

from typing import Iterable, Set
from enum import Enum
from kaiten.session import Session

import codecs


class Card():
    def __init__(self, card_json):
        self.__ggis_id__ = ''
        self.__data__ = card_json
        for key in card_json:
            setattr(self, key, card_json[key])

    @property
    def ggis_id(self):
        return self.__ggis_id__

    def ggis_id_from_title(self, tag, dots_size: int = 3):
        ggis_id_pos = self.title.find(tag)
        if ggis_id_pos >= 0:
            dot_count = 0
            for position, s in enumerate(self.title):
                if s == '.':
                    dot_count += 1
                    if dot_count == dots_size:
                        break
                position = position + 1
            self.__ggis_id__ = self.title[ggis_id_pos + len(tag) + 1:position]
        else:
            self.__ggis_id__ = ''

    def __str__(self):
        return '[' + str(self.id) + '] (' + self.ggis_id + ') ' + self.title

    def dump_json(self, file: str) -> None:
        with codecs.open(file, 'w', encoding='utf-8') as fp:
            json.dump(self.__data__, fp, ensure_ascii=False)

    @property
    def deadline(self):
        if self.due_date is None:
            return None
        return dateutil.parser.parse(self.due_date).date()

    @property
    def is_late(self):
        if self.deadline is None:
            return False
        return date.today() > self.deadline

    @property
    def raw(self):
        return self.__data__


# Утилиты для выборки всех карточек определённого вида

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


class CardType(Enum):
    Feature = 4
    User_story = 5
    Bug = 7
    Enabler = 8


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
    card_ident = f"{tag}.{identificator}"
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
