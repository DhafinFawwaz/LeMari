from sqlite3 import *
from typing import *
import os
from flet_core.file_picker import FilePickerFile
import shutil
from .seed import Seeder

class DB:
    conn: Connection
    cursor: Cursor
    is_initialized: bool = False
    db_path: str
    image_folder_path: str
    

    def init():
        if os.name == 'posix':
            data_home = os.getenv('XDG_DATA_HOME', os.path.join(os.path.expanduser('~'), '.local', 'share'))
        else: 
            data_home = os.getenv('APPDATA')

        database_dir = os.path.join(data_home, 'com.bercarat.le-mari')
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)

        DB.db_path = os.path.join(database_dir, 'database', 'database.db')
        if not os.path.exists(os.path.join(database_dir, 'database')):
            os.makedirs(os.path.join(database_dir, 'database'))

        DB.image_folder_path = os.path.join(database_dir, 'images')
        if not os.path.exists(DB.image_folder_path):
            os.makedirs(DB.image_folder_path)


        DB.conn = connect(DB.db_path, check_same_thread=False)
        DB.cursor = DB.conn.cursor()
        DB.create_tables()
        DB.is_initialized = True

        # Tells that if seeding have been done before
        # if not yet, go seed.
        one_of_the_seed_image = DB.get_image_path("red-jeans.png")
        if (not os.path.exists(one_of_the_seed_image)):
            seeder = Seeder()
            seeder.seed()
        

        

    def create_tables():
        DB.cursor.execute("""
CREATE TABLE IF NOT EXISTS cloth (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL UNIQUE,
    image_name TEXT NOT NULL UNIQUE
);
        """)
        DB.cursor.execute("""
CREATE TABLE IF NOT EXISTS outfit (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL UNIQUE
);
        """)
        DB.cursor.execute("""
CREATE TABLE IF NOT EXISTS tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL UNIQUE
);
        """)
        DB.cursor.execute("""
CREATE TABLE IF NOT EXISTS cloth_tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    cloth_id INTEGER,
    tag_id INTEGER, 
    FOREIGN KEY (cloth_id) REFERENCES cloth(id),
    FOREIGN KEY (tag_id) REFERENCES tag(id)
);
        """)
        DB.cursor.execute("""
CREATE TABLE IF NOT EXISTS outfit_cloth (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    outfit_id INTEGER,
    cloth_id INTEGER,
    FOREIGN KEY (outfit_id) REFERENCES outfit(id),
    FOREIGN KEY (cloth_id) REFERENCES cloth(id)
);
""")

    def save_image(image_file: FilePickerFile):
        shutil.copy2(image_file.path, DB.get_image_path(image_file.name))
    
    def delete_image_by_path_if_exist(image_path: str):
        pass

    def get_image_path(image_name):
        return os.path.join(DB.image_folder_path, image_name)
    

    def execute(query: str, params: Tuple = ()) -> Cursor:
        if not DB.is_initialized:
            DB.init()
        cursor = DB.cursor.execute(query, params)
        cursor.connection.commit()
        return cursor
    
    def executemany(query: str, params: List[Tuple] = ()) -> Cursor:
        if not DB.is_initialized:
            DB.init()

        cursor = DB.cursor.executemany(query, params)
        cursor.connection.commit()
        return cursor