from kaiten.user import User
import json

class Input_config:
    """!Конфигурация для создания карточек: доска, колонка, роль и тип карточки"""

    def __init__(self, config_name: str, owner: User, size: int = None):
        self.config = json.load(open('env/skird_config/' + config_name + '.json', encoding='utf-8'))
        self.config['owner_id'] = owner.id
        self.config['owner_email'] = owner.email
        if size is not None:
            self.config.json['size_text'] = f"{size} ч"

        for key in self.config:
            setattr(self, key, self.config[key])
        self.owner_id = owner.id
        self.owner_email = owner.email

    @property
    def json(self):
        return self.config
