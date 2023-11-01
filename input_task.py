from card import Card
from user import User
import requests

class Input_task:
    def __init__(self, title: str, owner: User, parent: Card, client):
        self.title = title
        self.parent = parent
        self.client = client

        create_card_parameters = {
            "title": self.correct_title,
            "board_id": 192,
            "size_text": '16 ч',
            "column_id": 776,
            "lane_id": 1275,

            "owner_id": owner.id,
            "owner_email": owner.email,
            "type_id": 6
        }
        self.client = client

        api_url = f"{self.client.base_api_url}/cards"
        create_request = requests.post(api_url, headers=self.client.headers, json=create_card_parameters)

        card = create_request.json()
        self.card_id = int(card['id'])

        print('Создана карточка: ' + self.complete_title(self.card_id))

        self.update_title(api_url)
        self.update_members(api_url, owner)
        self.update_parent(api_url, parent)
        self.update_tag(api_url)

    @property
    def correct_title(self) -> str:
        return '[CAD]:TS.' + self.parent.ggis_id + '.-----. ' + self.title 
    
    def complete_title(self, card_id) -> str:
        return '[CAD]:TS.' + self.parent.ggis_id + '.' + str(card_id) + '. ' + self.title 

    def update_tag(self, url):
        tags_url = url + '/' + str(self.card_id) + '/tags'
        add_ggis_tag_parameters = {
            "name": "ГГИС"
        }
        requests.post(tags_url, headers=self.client.headers, json=add_ggis_tag_parameters)

    def update_parent(self, url, parent):
        children_url = url + '/' + str(parent.id) + '/children'
        add_child_card = {
            "card_id": self.card_id
        }
        requests.post(children_url, headers=self.client.headers, json=add_child_card)

    def update_members(self, url, owner):
        members_url = url + '/' + str(self.card_id) + '/members'
        add_member_parameters = {
            "user_id": owner.id
        }
        requests.post(members_url, headers=self.client.headers, json=add_member_parameters)

        responsible_url = url + '/' + str(self.card_id) + '/members/' + str(owner.id)
        make_responsible_parameters = {
            "type": 2
        }
        requests.patch(responsible_url, headers=self.client.headers, json=make_responsible_parameters)

    def update_title(self, url):
        card_api_path = url + '/' + str(self.card_id)
        update_title_parameters = {
            "title": self.complete_title(self.card_id)
        }
        requests.patch(card_api_path, headers=self.client.headers, json=update_title_parameters)
