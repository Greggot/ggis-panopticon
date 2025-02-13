from kaiten.card import Card
from kaiten.session import Session
from card_creator_config import Card_creator_config
import requests
from enum import Enum, IntEnum

class Task_Type(Enum):
    delivery = 6
    discovery = 11

# 1 - просто участник, 2 - ответственный
class Responsibility(IntEnum):
    member = 1
    owner = 2

class Card_creator:
    def __init__(self, title: str, config: Card_creator_config, parent: Card, session: Session):
        self.title = title
        self.session = session
        self.parent = parent
        self.card_id = 0

        self.card_type = Task_Type(config.json['type_id'])
        config.json['title'] = self.complete_title
        create_request = requests.post(session.cards_url, headers=self.session.headers, json=config.json)
        self.card_id = int(create_request.json()['id'])

        print(f"Создана карточка: \"{self.complete_title}\"  --> {self.session.server}/{self.card_id}")

        self.set_correct_title()
        self.add_member_and_make_responsible(config.owner_id)
        self.link_to_parent_card()
        self.add_tag('ГГИС')
        self.add_tag('C++')

    @property
    def complete_title(self) -> str:
        if self.card_type == Task_Type.delivery or self.card_type == Task_Type.discovery:
            return f'[CAD]:TS.{self.parent.ggis_id}.{self.card_id}. {self.title}'

    def set_correct_title(self):
        requests.patch(self.session.card_url(self.card_id), headers=self.session.headers, json={
            "title": self.complete_title
        })

    def add_tag(self, name: str):
        requests.post(self.session.tags_url(self.card_id), headers=self.session.headers, json={
            "name": name
        })

    def link_to_parent_card(self):
        requests.post(self.session.children_url(self.parent.id), headers=self.session.headers, json={
            "card_id": self.card_id
        })

    def add_member_and_make_responsible(self, owner_id: int):
        requests.post(self.session.member_url(self.card_id), headers=self.session.headers, json={
            "user_id": owner_id
        })
        requests.patch(self.session.member_url(self.card_id, owner_id), headers=self.session.headers, json={
            "type": Responsibility.owner
        })
