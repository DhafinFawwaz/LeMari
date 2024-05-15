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



    def generate_cloths(self, cloths: List[Tuple[str, str]]):
        
        for idx in range(len(cloths)):
            cloth_name = cloths[idx][0].split(".")[0]
            self.__download(cloths[idx][1], cloths[idx][0])
            self.cursor.execute("INSERT INTO cloth (id, name, image_name) VALUES (?, ?, ?)", (idx, cloth_name, cloths[idx][0]))
        
        self.conn.commit()
        

    def __download(self, url: str, name: str):
        response = requests.get(url)
        
        response.raise_for_status()

        destination = os.path.join(self.image_folder_path, name)
        with open(destination, 'wb') as f:
            f.write(response.content)
        
        print(f"Put {name}.")

    def fetch_data(self, table_name: str):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        return rows

        
if __name__ == "__main__":
    seeder = Seeder()
    seeder.seed()

    