from card import Card
from kaiten.session import Session
from input_config import Input_config
import requests
from enum import Enum


class Task_Type(Enum):
    delivery = 6
    discovery = 11


class Input_task:
    def __init__(self, title: str, config: Input_config, parent: Card, session: Session, size: int = None):
        self.title = title
        self.session = session
        self.parent = parent
        self.card_id = 0

        create_card_parameters = config.json
        self.card_type = Task_Type(create_card_parameters['type_id'])
        create_card_parameters['title'] = self.complete_title
        if size is not None:
            create_card_parameters['size_text'] = f"{size} ч"
        create_request = requests.post(session.cards_url, headers=self.session.headers, json=config.json)

        card = create_request.json()
        self.card_id = int(card['id'])

        print('Создана карточка: ' + self.complete_title)

        self.set_correct_title()
        self.add_member_and_make_responsible(config.owner_id)
        self.link_to_parent_card()
        self.add_tag('ГГИС')
        self.add_tag('C++')

    @property
    def complete_title(self) -> str:
        if self.card_type == Task_Type.delivery:
            return f'[CAD]:TS.{self.parent.ggis_id}.{self.card_id}. {self.title}'

        if self.card_type == Task_Type.discovery:
            return f'[CAD]:TD.{self.parent.ggis_id}.{self.card_id}. {self.title}'

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
        # 1 - просто участник, 2 - ответственный
        requests.patch(self.session.member_url(self.card_id, owner_id), headers=self.session.headers, json={
            "type": 2
        })
