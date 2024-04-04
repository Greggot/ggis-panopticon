
class Session:
    def __init__(self, server: str, token: str) -> None:
        self.server = server
        self.token = token

    @property
    def headers(self):
        return {
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }

    @property
    def url(self) -> str:
        return f'{self.server}/api/latest'
    
    @property
    def cards_url(self) -> str:
        return f'{self.url}/cards'
    
    def card_url(self, card_id: int) -> str:
        return f'{self.cards_url}/{card_id}'
    
    def member_url(self, card_id: int, member: int | None = None) -> str:
        members_url = f'{self.cards_url}/{card_id}/members'
        if member is None:
            members_url
        return f'{members_url}/{member}'
    
    def children_url(self, card_id: int) -> str:
        return f'{self.cards_url}/{card_id}/children'
    
    def tags_url(self, card_id: int) -> str:
        return f'{self.cards_url}/{card_id}/tags'

    def time_logs_url(self, card_id: int) -> str:
        return f'{self.cards_url}/{card_id}/time-logs'
    
    @property
    def current_user_url(self) -> str:
        return f'{self.url}/users/current'