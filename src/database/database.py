from sqlite3 import *
from typing import *
import os
from flet_core.file_picker import FilePickerFile
import shutil

class DB:
    conn: Connection
    cursor: Cursor
    is_initialized: bool = False
    db_path: str
    image_folder_path: str
    

    def init():
        database_dir = '%s\\com.bercarat.le-mari\\' %  os.environ['APPDATA'] 
        if not os.path.exists(database_dir):
            os.makedirs(database_dir)

        DB.db_path = '%sdatabase\\database.db' % database_dir
        if not os.path.exists('%sdatabase' % database_dir):
            os.makedirs('%sdatabase' % database_dir)

        DB.image_folder_path = '%simages' % database_dir
        if not os.path.exists(DB.image_folder_path):
            os.makedirs(DB.image_folder_path)


        DB.conn = connect(DB.db_path, check_same_thread=False)
        DB.cursor = DB.conn.cursor()
        DB.create_tables()
        DB.is_initialized = True
        

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
        return '%s\\%s' % (DB.image_folder_path, image_name)
    

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