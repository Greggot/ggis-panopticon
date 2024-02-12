import requests
import json
import dateutil
from datetime import date

from typing import Iterable
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

def cards_type_request(session: Session, type_id: int, offset: int = 0):
    request = requests.get(session.cards_url, headers=session.headers, params={
        "type_ids" : type_id,
        "condition": 1,
        "offset": offset
    })
    return request.json()

def cards_of_type(session: Session, type_id: int, offset: int = 0) -> list:
    offset = 0
    full_list = []
    temp_list = cards_type_request(session, type_id, offset)
    while len(temp_list) == 100:
        offset += 100
        full_list += temp_list
        temp_list = cards_type_request(session, type_id, offset)
    full_list += temp_list
    return full_list

class Card_type(Enum):
    Feature = 4
    User_story = 5
    Bug = 7
    Enabler = 8

def cards_of_ggis_id(session: Session, type_id: Card_type, id_tag: str) -> Iterable[Card]:
    card_list = []
    full_list = cards_of_type(session, type_id.value)
    for member in  full_list:
        card = Card(member)
        if card.title.find(id_tag, 0) >= 0:
            card.ggis_id_from_title(id_tag)
            card_list.append(card)
    card_list.sort(key=lambda card: card.id)
    print('Finished search of ', id_tag)
    return card_list

def features(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, Card_type.Feature, ':F')

def user_stories(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, Card_type.User_story, ':US')

def enablers(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, Card_type.Enabler, ':EN')

def bugs(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, Card_type.Bug, ':BUG')