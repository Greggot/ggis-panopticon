import requests
from card import Card

class User():
    def __init__(self, client):
        api_url = f"{ client.base_api_url}/users/current"
        request = requests.get(api_url, headers=client.headers)
        self.__client__ = client
        self.__headers__ = client.headers
        self.__data__ = request.json()

    def __str__(self):
        return '[' + str(self.id) + ']' + self.name + ' - ' + self.email
    
    def card_list(self, condition: int = 1) -> list:
        api_url = f"{self.__client__.base_api_url}/cards"
        parameters = {
            "member_ids": str(self.id),
            "condition": condition
        }
        request = requests.get(api_url, headers=self.__client__.headers, params=parameters)
        card_list = []
        for member in request.json():
            card = Card(member)
            card_list.append(card)
        return card_list
    
    def column_card_list(self, name: str = 'В работе') -> list:
        parameters = {
            "member_ids": str(self.id),
            "condition": 1
        }
        request = requests.get(self.__card_url__(), headers=self.__headers__, params=parameters)
        card_list = []
        for member in request.json():
            card = Card(member)
            column = card.column
            if column['title'] == name:
                card_list.append(card)
        return card_list
    
    def parentless_cards(self) -> list:
        parameters = {
            "member_ids": str(self.id),
            "condition": 1
        }
        request = requests.get(self.__card_url__(), headers=self.__headers__, params=parameters)
        card_list = []
        for member in request.json():
            card = Card(member)
            if card.parents_count == 0:
                card_list.append(card)
        return card_list

    @property
    def id(self):
        return self.__data__['id']
    
    @property
    def name(self):
        return self.__data__['full_name']
    
    @property
    def email(self):
        return self.__data__['email']
    
    
    def __card_url__(self):
        return f"{self.__client__.base_api_url}/cards"