from typing import List

class Tag:
    def __init__(self, name: str, id: int=-1):
        self.id = id
        self.name = name

    def get_all() -> List["Tag"]:
        return []
        
