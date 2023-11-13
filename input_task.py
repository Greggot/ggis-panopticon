from card import Card
from user import User
from kaiten.session import Session
import requests

class Input_task:
    def __init__(self, title: str, owner: User, parent: Card, session: Session):
        self.title = title
        self.session = session
        self.parent = parent
        self.card_id = 0

        create_card_parameters = {
            "title": self.complete_title,
            "board_id": 192,
            "size_text": '16 ч',
            "column_id": 776,
            "lane_id": 1275,

            "owner_id": owner.id,
            "owner_email": owner.email,
            "type_id": 6,

            # C++ custom role
            "properties": { 
                "id_19": "1"
            }
        }
        create_request = requests.post(session.cards_url, headers=self.session.headers, json=create_card_parameters)

        card = create_request.json()
        self.card_id = int(card['id'])

        print('Создана карточка: ' + self.complete_title)

        self.set_correct_title()
        self.add_member_and_make_responsible(owner)
        self.link_to_parent_card()
        self.add_tag('ГГИС')

    @property
    def complete_title(self) -> str:
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

    def add_member_and_make_responsible(self, owner: Card):
        requests.post(self.session.member_url(self.card_id), headers=self.session.headers, json={
            "user_id": owner.id
        })
        # 1 - просто участник, 2 - ответственный
        requests.patch(self.session.member_url(self.card_id, owner.id), headers=self.session.headers, json={
            "type": 2
        })
