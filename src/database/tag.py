from typing import List
from sqlite3 import Cursor
from database.database import DB


class Tag:
    def __init__(self, name: str, id: int = -1):
        self.id = id
        self.name = name

    def __str__(self):
        return str((self.id, self.name))

    def save(self):
        print(f"save {self.name}")
        cursor = DB.execute("INSERT INTO tag (name) VALUES (?)", (self.name,))
        self.id = cursor.lastrowid

    def delete(self):
        cursor = DB.execute("DELETE FROM tag WHERE id = ?", (self.id,))

    def update(self,name:str):
        self.name = name
        cursor = DB.execute("UPDATE tag SET name = ? WHERE id = ?", (self.name,self.id))

    def get_all() -> List["Tag"]:
        cursor: Cursor = DB.execute("SELECT * FROM tag")
        res = cursor.fetchall()
        print(f"Hasil res {res}")
        tag_list: List[Tag] = []
        for row in res:
            print(row)
            tag_list.append(Tag(name=row[1], id=row[0]))
        return tag_list
