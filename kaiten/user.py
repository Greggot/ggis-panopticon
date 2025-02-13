from kaiten.card import Card
from typing import Iterable
from kaiten.session import Session
import requests

class User():
    def __init__(self, session: Session):
        self.session = session
        request = requests.get(self.session.current_user_url, headers=session.headers)
        for key in request.json():
            setattr(self, key, request.json()[key])

    def __str__(self):
        return '[' + str(self.id) + ']' + self.full_name + ' - ' + self.email
    
    def card_list(self, condition: int = 1) -> Iterable[Card]:
        request = requests.get(self.session.cards_url, headers=self.session.headers, params={
            "member_ids": str(self.id),
            "condition": condition
        })
        for card in (Card(member) for member in request.json()):
            yield card
    
    def column_card_list(self, name: str = 'В работе') -> Iterable[Card]:
        request = requests.get(self.session.cards_url, headers=self.session.headers, params={
            "member_ids": str(self.id),
            "condition": 1
        })
        for card in (Card(member) for member in request.json()):
            if card.column['title'] == name:
                yield card
    
    def parentless_cards(self) -> Iterable[Card]:
        request = requests.get(self.session.cards_url, headers=self.session.headers, params={
            "member_ids": str(self.id),
            "condition": 1
        })
        for card in (Card(member) for member in request.json()):
            if card.parents_count == 0:
                yield card
    