import json
import codecs
import dateutil
import dateutil.parser

from datetime import date
from enum import Enum

class Card:
    def __init__(self, card_json):
        self.__ggis_id__ = ''
        self.__data__ = card_json
        for key in card_json:
            setattr(self, key, card_json[key])

    @property
    def ggis_id(self):
        return self.__ggis_id__

    def ggis_id_from_title(self, tag, dots_size: int = 3):
        ggis_id_pos = self.title.find(tag)
        if ggis_id_pos >= 0:
            dot_count = 0
            for position, s in enumerate(self.title):
                if s == '.':
                    dot_count += 1
                    if dot_count == dots_size:
                        break
                position = position + 1
            self.__ggis_id__ = self.title[ggis_id_pos + len(tag) + 1:position]
        else:
            self.__ggis_id__ = ''

    def __str__(self):
        return '[' + str(self.id) + '] (' + self.ggis_id + ') ' + self.title

    def dump_json(self, file: str) -> None:
        with codecs.open(file, 'w', encoding='utf-8') as fp:
            json.dump(self.__data__, fp, ensure_ascii=False)

    @property
    def deadline(self):
        if self.due_date is None:
            return None
        return dateutil.parser.parse(self.due_date).date()

    @property
    def is_late(self):
        if self.deadline is None:
            return False
        return date.today() > self.deadline

    @property
    def raw(self):
        return self.__data__
    
class CardType(Enum):
    Feature = 4
    User_story = 5
    Bug = 7
    Enabler = 8
