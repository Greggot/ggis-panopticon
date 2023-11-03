import requests
from typing import List, Iterable
from enum import Enum

class Card():
    def __init__(self, card_json):
        self.__data__ = card_json
        self.__ggis_id__ = ''

    @property
    def ggis_id(self):
        return self.__ggis_id__

    def ggis_id_from_title(self, tag, dots: int = 3):
        ggis_id_pos = self.title.find(tag)
        if ggis_id_pos >= 0:
            index = 0
            position = 0
            for s in self.title:
                if s == '.':
                    index = index + 1
                    if index == dots:
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

    @property
    def parents_count(self):
        return self.__data__['parents_count']
    
    @property
    def owner(self):
        return self.__data__['owner']
    
    @property
    def id(self):
        return self.__data__['id']
    
    @property
    def title(self):
        return self.__data__['title']
    
    @property
    def column(self):
        return self.__data__['column']
    
    @property
    def parents_ids(self):
        return self.__data__['parents_ids']
    
# Утилиты для выборки всех карточек определённого вида

def cards_of_type(session: Session, type_id: int) -> list:
    request = requests.get(session.cards_url, headers=session.headers, params={
        "type_ids" : type_id
    })
    print(request)
    return request.json()

class Card_type(Enum):
    Feature = 4
    User_story = 5
    Bug = 7
    Enabler = 8

def cards_of_ggis_id(client: Session, type_id: Card_type, id_tag: str) -> Iterable[Card]:
    card_list = []
    full_list = cards_of_type(client.cards_url, type_id.value)
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