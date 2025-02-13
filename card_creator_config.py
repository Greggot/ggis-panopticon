from kaiten.user import User
import json

# TODO: Сделать json методом, чтобы он находу собирал объект,
# чтобы не обращаться к object.config['member'] вместо object.member 
#
# TODO: Добавить список тегов в конфиг, чтобы он не был захардкожен
class Card_creator_config:
    """!Конфигурация для создания карточек: доска, колонка, роль и тип карточки"""

    def __init__(self, config_name: str, owner: User, size: int = None):
        self.config = json.load(open('env/skird_config/' + config_name + '.json', encoding='utf-8'))
        self.config['owner_id'] = owner.id
        self.config['owner_email'] = owner.email
        if size is not None:
            self.config['size_text'] = f"{size} ч"
        for key in self.config:
            setattr(self, key, self.config[key])

    @property
    def json(self):
        return self.config
