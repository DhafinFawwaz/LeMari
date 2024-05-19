from database.database import DB
from database.tag import Tag
from sqlite3 import Cursor
from database.cloth import Cloth
from typing import List
from flet_core.file_picker import FilePickerFile
import json

class Outfit:
    def __init__(self, name: str, cloth_list: List[Cloth], id: int = -1):
        self.id = id
        self.name = name
        self.cloth_list = cloth_list

    def save(self):
        cursor: Cursor = DB.execute("INSERT INTO outfit (name) VALUES (?)", (self.name,))
        self.id = cursor.lastrowid
        params = [(self.id, cloth.id) for cloth in self.cloth_list]
        DB.executemany("INSERT INTO outfit_cloth (outfit_id, cloth_id) VALUES (?, ?)", params)

    def delete(self):
        DB.execute("DELETE FROM outfit_cloth WHERE outfit_id = ?", (self.id,))
        DB.execute("DELETE FROM outfit WHERE id = ?", (self.id,))

    def edit(self):
        DB.execute("UPDATE outfit SET name = ? WHERE id = ?", (self.name, self.id))
        DB.execute("DELETE FROM outfit_cloth WHERE outfit_id = ?", (self.id,))

        params = [(self.id, cloth.id) for cloth in self.cloth_list]
        DB.executemany("INSERT INTO outfit_cloth (outfit_id, cloth_id) VALUES (?, ?)", params)
    
    def cloth_list_from_json(cloth_json: str) -> List[Cloth]:
        loaded = json.loads(cloth_json)
        return [Cloth(name=loaded_cloth['name'], id=loaded_cloth['id'], tag_list=[], image_name=loaded_cloth['image_name']) for loaded_cloth in loaded if loaded_cloth['id'] != None]

    def get_all_by_search(search_filter: str) -> List["Outfit"]:
        outfit_list = Outfit.get_all_outfit()
        if len(search_filter) > 0:
            outfit_list = [outfit for outfit in outfit_list if search_filter.lower() in outfit.name.lower()]
        return outfit_list
    
    def get_cloth_list(self) -> List["Cloth"]:
        cursor: Cursor = DB.execute("""
SELECT cloth.id, cloth.name, cloth.image_name,
json_group_array(json_object('id', tag.id, 'name', tag.name)) as tagList
FROM outfit_cloth
INNER JOIN cloth ON outfit_cloth.cloth_id = cloth.id
LEFT JOIN cloth_tag ON cloth.id = cloth_tag.cloth_id
LEFT JOIN tag ON cloth_tag.tag_id = tag.id
WHERE outfit_cloth.outfit_id = ?
GROUP BY cloth.id
ORDER BY cloth.name
""", (self.id,))
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

    def get_all_outfit() -> List["Outfit"]:
        cursor: Cursor = DB.execute("""
SELECT outfit.id, outfit.name, 
json_group_array(json_object('id', cloth.id, 'name', cloth.name, 'image_name', cloth.image_name)) as clothList
from outfit
LEFT JOIN outfit_cloth ON outfit.id = outfit_cloth.outfit_id
LEFT JOIN cloth ON outfit_cloth.cloth_id = cloth.id
GROUP BY outfit.id
ORDER BY outfit.name
""")
        res = cursor.fetchall()
        outfit_list: List[Outfit] = []
        for row in res:
            outfit = Outfit(
                id=row[0],
                name=row[1],
                cloth_list=Outfit.cloth_list_from_json(row[2])
            )
            outfit_list.append(outfit)
        return outfit_list
            