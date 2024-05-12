from database.database import DB
from database.tag import Tag
from database.cloth import Cloth
from typing import List

class Outfit:
    def __init__(self, name: str, cloth_list: List[Cloth]):
        self.id = -1
        self.name = name
        self.cloth_list = cloth_list
