from database.database import DB
from database.tag import Tag
from typing import List

class Cloth:
    def __init__(self, name: str, image_name: str, tag_list: List[Tag]):
        self.id = -1
        self.name = name
        self.image_name = image_name
        self.tags = tag_list

    # return the image path that can be used in the Image flet component
    def get_image_path(self):
        return DB.get_image_path(self.image_name)