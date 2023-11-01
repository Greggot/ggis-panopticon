import requests

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
    
def all_cards_with_type(client, type_id: int) -> list:
    api_url = f"{client.base_api_url}/cards"
    parameters = {
        "type_ids" : type_id
    }
    request = requests.get(api_url, headers=client.headers, params=parameters)
    return request.json()

def all_cards_from_board(client, board_id: int) -> list:
    api_url = f"{client.base_api_url}/cards"
    parameters = {
        "board_id" : board_id
    }
    request = requests.get(api_url, headers=client.headers, params=parameters)
    return request.json()

def features(client) -> list:
    card_list = []
    full_list = all_cards_with_type(client, 4)
    for member in  full_list:
        card = Card(member)
        if card.title.find(':F', 0) >= 0:
            card.ggis_id_from_title(':F')
            card_list.append(card)
    card_list.sort(key=lambda card: card.id)
    return card_list

def user_stories(client) -> list:
    card_list = []
    full_list = all_cards_with_type(client, 5)
    for member in  full_list:
        card = Card(member)
        if card.title.find(':US') >= 0:
            card.ggis_id_from_title(':US')
            card_list.append(card)
    card_list.sort(key=lambda card: card.id)
    return card_list

def enablers(client) -> list:
    card_list = []
    full_list = all_cards_with_type(client, 8)
    for member in  full_list:
        card = Card(member)
        if card.title.find(':EN') >= 0:
            card.ggis_id_from_title(':EN')
            card_list.append(card)
    card_list.sort(key=lambda card: card.id)
    return card_list

def bugs(client) -> list:
    card_list = []
    full_list = all_cards_with_type(client, 7)
    for member in  full_list:
        card = Card(member)
        if card.title.find(':BUG') >= 0:
            card.ggis_id_from_title(':BUG')
            card_list.append(card)
    card_list.sort(key=lambda card: card.id)
    return card_list