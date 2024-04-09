import requests
from card import Card
from typing import Iterable
from kaiten.session import Session
import asyncio

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

    async def gather(self, cond):
        return requests.get(self.session.cards_url, headers=self.session.headers, params={
            # "member_ids": str(self.id),
            "offset": cond

        })

    # for card in asyncio.run(user.es_plus_plus_cards()):
    #         print('  ', card)
    async def es_plus_plus_cards(self) -> Iterable[Card]:
        tasks = []
        for i in range(0, 2000, 100):
            tasks.append(asyncio.create_task(self.gather(i)))
        responses = await asyncio.gather(*tasks)
        res = []
        for response in responses:
            for card in (Card(member) for member in response.json()):
                for tag_description in card.__dict__.get('tags', {}):
                    if ('name', 'С++') in tag_description.items():
                        res.append(card)
        return res
    