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

    def __str__(self):
        return str((self.id, self.name, self.image_name, self.tag_list))

    # return the image path that can be used in the Image flet component
    def get_image_path(self):
        return DB.get_image_path(self.image_name)
    
    def save(self):
        cursor: Cursor = DB.execute("INSERT INTO cloth (name, image_name) VALUES (?, ?)", (self.name, self.image_name))
        self.id = cursor.lastrowid
        params = [(self.id, tag.id) for tag in self.tag_list]
        DB.executemany("INSERT INTO cloth_tag (cloth_id, tag_id) VALUES (?, ?)", params)
    
    def get_all() -> List["Cloth"]:
        cursor: Cursor = DB.execute("""
SELECT cloth.id, cloth.name, cloth.image_name,
json_group_array(json_object('id', tag.id, 'name', tag.name)) as tagList
FROM cloth
LEFT JOIN cloth_tag ON cloth.id = cloth_tag.cloth_id
LEFT JOIN tag ON cloth_tag.tag_id = tag.id
GROUP BY cloth.id
ORDER BY cloth.name
""")
        res = cursor.fetchall()
        cloth_list: List[Cloth] = []
        for row in res:
            cloth = Cloth(
                id=row[0],
                name=row[1],
                image_name=row[2],
                tag_list=Cloth.tag_list_from_json(row[3])
            )
            cloth_list.append(cloth)
        return cloth_list
    
    def save_image(image_file: FilePickerFile):
        DB.save_image(image_file)
    def delete_image_by_name(image_name: str):
        DB.delete_image_by_path_if_exist(DB.get_image_path(image_name))

    def tag_list_from_json(tag_json: str) -> List[Tag]:
        loaded = json.loads(tag_json)
        return [Tag(name=loaded_tag['name'], id=loaded_tag['id']) for loaded_tag in loaded if loaded_tag['id'] != None]
        

    def find_all_by_search_and_tags(search_filter: str, tag_list_filter: List[Tag]) -> List["Cloth"]:
        cloth_list = Cloth.get_all()
        if len(search_filter) > 0:
            cloth_list = [cloth for cloth in cloth_list if search_filter.lower() in cloth.name.lower()]
        if len(tag_list_filter) > 0:
            tag_filter_id_list = [tag.id for tag in tag_list_filter]
            res = []
            for cloth in cloth_list:
                for tag in cloth.tag_list:
                    if tag.id in tag_filter_id_list:
                        res.append(cloth)
                        break
            return res
        return cloth_list
    
    def edit(self):
        # update cloth name and image name
        DB.execute("UPDATE cloth SET name = ?, image_name = ? WHERE id = ?", (self.name, self.image_name, self.id))
        
        # delete all cloth_tag associated with this cloth
        DB.execute("DELETE FROM cloth_tag WHERE cloth_id = ?", (self.id,))
        
        # insert all cloth_tag associated with this cloth
        params = [(self.id, tag.id) for tag in self.tag_list]
        DB.executemany("INSERT INTO cloth_tag (cloth_id, tag_id) VALUES (?, ?)", params)

    def delete(self):
        DB.execute("DELETE FROM cloth_tag WHERE cloth_id = ?", (self.id,))
        DB.execute("DELETE FROM cloth WHERE id = ?", (self.id,))
