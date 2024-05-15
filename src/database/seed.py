from sqlite3 import *
from typing import *
import os
import requests

class Seeder(): 
    conn: Connection
    cursor: Cursor
    is_initialized: bool
    db_path: str
    image_folder_path: str
    

    def __init__(self):
        if os.name == 'posix':
            data_home = os.getenv('XDG_DATA_HOME', os.path.join(os.path.expanduser('~'), '.local', 'share'))
        else: 
            data_home = os.getenv('APPDATA')

        database_dir = os.path.join(data_home, 'com.bercarat.le-mari')
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)

        self.db_path = os.path.join(database_dir, 'database', 'database.db')
        if not os.path.exists(os.path.join(database_dir, 'database')):
            os.makedirs(os.path.join(database_dir, 'database'))

        self.image_folder_path = os.path.join(database_dir, 'images')
        if not os.path.exists(self.image_folder_path):
            os.makedirs(self.image_folder_path)


        self.conn = connect(self.db_path)
        self.cursor = self.conn.cursor()

    def seed(self):
        # Seeding cloths table
        CLOTHS = [
            ("power-ranger.png", "https://drive.google.com/uc?export=download&id=1NInFNKDGuRrpFn80Xovldyn8WxmMJd4P"),
            ("firefighter.png", "https://drive.google.com/uc?export=download&id=1dd-3J21YVqAhEgQFxBKEWUzlslXf7Y97"),
            ("shirt.png", "https://drive.google.com/uc?export=download&id=1KbUMxKpBLzlS8J4_gvqjkFyeOdyDxhl9"),
            ("lion-tshirt.png", "https://drive.google.com/uc?export=download&id=12WE19uU4a0iHCz__gRiE1SIwr9-GRz7q"),
            ("full-cloth.png", "https://drive.google.com/uc?export=download&id=1GjxaZpL-QYOM5U13ICoFIFJWrXB4ElzG"),
            ("overalls.png", "https://drive.google.com/uc?export=download&id=1DZlgzfhX1w2Hm1U87_gbxvhIMMZtMitt"),
            ("best-jeans.png", "https://drive.google.com/uc?export=download&id=1uOf55tPcHpSrQhm7b2EA8EkiIONowd8n"),
            ("blue-shirt.png", "https://drive.google.com/uc?export=download&id=1tYSFrakSJmRnBvEIeC4vbK6-ibG-hP64"),
            ("red-skirt.png", "https://drive.google.com/uc?export=download&id=1smGtx3ahmoX7MWDpKmNZlh4CfOJkKPv6"),
            ("red-jeans.png", "https://drive.google.com/uc?export=download&id=1-cm4IFqJ_JJmOesk6NumU5c3JwfoOLUN")
        ]

        self.generate_cloths(CLOTHS)

        TAGS = ["Superhero", "Unique", "Freak", "Casual", "Classic", "Elegant", "Sporty", "Formal", "Sexy"]

        self.generate_tags(TAGS)

        OUTFITS = ["Superhero Outfit", "Casual Outfit", "Classic Outfit", "Overall", "Fire Fighter"]

        self.generate_outfits(OUTFITS)

        # This cloth_tags relation is absolutely random.
        CLOTH_TAGS = [
            (0, 0), (1, 0), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3)
        ]

        self.generate_cloth_tags(CLOTH_TAGS)

        # This is absolutely random too.
        OUTFIT_CLOTHS = [
            (0, 0), (0, 1), (1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9)
        ]

        self.generate_outfit_cloths(OUTFIT_CLOTHS)





    def generate_cloths(self, cloths: List[Tuple[str, str]]):
        
        for idx in range(len(cloths)):
            cloth_name = cloths[idx][0].split(".")[0]
            self.__download(cloths[idx][1], cloths[idx][0])

            self.cursor.execute("INSERT INTO cloth (id, name, image_name) VALUES (?, ?, ?)", (idx, cloth_name, cloths[idx][0]))
        
        self.conn.commit()

    
    def generate_tags(self, tags: List[str]):
        for idx in range(len(tags)):
            self.cursor.execute("INSERT INTO tag (id, name) VALUES (?, ?)", (idx, tags[idx]))
        
        self.conn.commit()

    def generate_outfits(self, outfits: List[str]):
        for idx in range(len(outfits)):
            self.cursor.execute("INSERT INTO outfit (id, name) VALUES (?, ?)", (idx, outfits[idx]))
        
        self.conn.commit()

    def generate_cloth_tags(self, cloth_tags: List[Tuple[int, int]]):
        for idx in range(len(cloth_tags)):
            self.cursor.execute("INSERT INTO cloth_tag (id, cloth_id, tag_id) VALUES (?, ?, ?)", (idx, cloth_tags[idx][0], cloth_tags[idx][1]))
        
        self.conn.commit()
    
    def generate_outfit_cloths(self, outfit_cloths: List[Tuple[int, int]]):
        for idx in range(len(outfit_cloths)):
            self.cursor.execute("INSERT INTO outfit_cloth (id, outfit_id, cloth_id) VALUES (?, ?, ?)", (idx, outfit_cloths[idx][0], outfit_cloths[idx][1]))
        
        self.conn.commit()


        

    def __download(self, url: str, name: str):
        response = requests.get(url)
        
        response.raise_for_status()

        destination = os.path.join(self.image_folder_path, name)
        with open(destination, 'wb') as f:
            f.write(response.content)
        
        print(f"Put {name} .")

    def fetch_data(self, table_name: str):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        return rows

    def clear(self): 
        self.cursor.execute("DELETE FROM cloth_tag")
        self.cursor.execute("DELETE FROM outfit_cloth")
        self.cursor.execute("DELETE FROM tag")
        self.cursor.execute("DELETE FROM outfit")
        self.cursor.execute("DELETE FROM cloth")
        self.conn.commit()
        
if __name__ == "__main__":
    seeder = Seeder()
    seeder.clear()
    print(seeder.fetch_data("cloth"))

    