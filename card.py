import requests
from typing import Iterable
from enum import Enum
from kaiten.session import Session

class Card():
    def __init__(self, card_json):
        self.__ggis_id__ = ''
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

    @property
    def raw(self):
        return self.__data__
    
# Утилиты для выборки всех карточек определённого вида

def cards_of_type(session: Session, type_id: int) -> list:
    request = requests.get(session.cards_url, headers=session.headers, params={
        "type_ids" : type_id
    })
    return request.json()

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
    return card_list

def features(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, Card_type.Feature, ':F')

def user_stories(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, Card_type.User_story, ':US')

def enablers(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, Card_type.Enabler, ':EN')

def bugs(session: Session) -> Iterable[Card]:
    return cards_of_ggis_id(session, Card_type.Bug, ':BUG')