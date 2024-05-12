from src.database.database import DB
from sqlite3 import *
import secrets

class TestDatabase:

    def test_insert_cloth(self):
        DB.init()
        prefix_1 = secrets.token_hex(8)
        prefix_2 = secrets.token_hex(8)
        prefix_3 = secrets.token_hex(8)
        values = [
            (f'{prefix_1}_1', f'{prefix_1}_image_1.png'),
            (f'{prefix_2}_2', f'{prefix_2}_image_2.jpg'),
            (f'{prefix_3}_3', f'{prefix_3}_image_3.webp')
        ]

        DB.execute(f"INSERT INTO cloth (name, image_name) VALUES ('{values[0][0]}', '{values[0][1]}'), ('{values[1][0]}', '{values[1][1]}'), ('{values[2][0]}', '{values[2][1]}')")
        cursor: Cursor = DB.execute(f"SELECT * FROM cloth WHERE name = '{values[0][0]}' OR name = '{values[1][0]}' OR name = '{values[2][0]}'")
        res = cursor.fetchall()
        assert any([x[1] == values[0][0] and x[2] == values[0][1] for x in res])
        assert any([x[1] == values[1][0] and x[2] == values[1][1] for x in res])
        assert any([x[1] == values[2][0] and x[2] == values[2][1] for x in res])

        DB.execute(f"DELETE FROM cloth WHERE name = '{values[0][0]}' OR name = '{values[1][0]}' OR name = '{values[2][0]}'")
    
        


