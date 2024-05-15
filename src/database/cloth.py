from database.database import DB
from sqlite3 import Cursor
from database.tag import Tag
from typing import List
from flet_core.file_picker import FilePickerFile
import json

class Cloth:
    def __init__(self, name: str, image_name: str, tag_list: List[Tag], id: int = -1):
        self.id = id
        self.name = name
        self.image_name = image_name
        self.tag_list = tag_list

    # return the image path that can be used in the Image flet component
    def get_image_path(self):
        return DB.get_image_path(self.image_name)
    
    def save(self):
        pass
    
    def get_all() -> List["Cloth"]:
        return []
    
    def save_image(image_file: FilePickerFile):
        pass
    def delete_image_by_name(image_name: str):
        pass

    def tag_list_from_json(tag_json: str) -> List[Tag]:
        return []
        

    def find_all_by_search_and_tags(search_filter: str, tag_list_filter: List[Tag]) -> List["Cloth"]:
        return []
    
    def edit(self):
        pass

    def delete(self):
        pass
