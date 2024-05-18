from sqlite3 import Cursor
import secrets
from typing import List, Tuple

from src.database.database import DB
from src.database.tag import Tag


class TestTag:

    def insert_seed_data(self) -> Tuple[str, str, str]:
        tag_name_1 = secrets.token_hex(8)
        tag_name_2 = secrets.token_hex(8)
        tag_name_3 = secrets.token_hex(8)

        DB.execute("INSERT INTO tag (name) VALUES (?), (?), (?)", (tag_name_1, tag_name_2, tag_name_3))

        cursor: Cursor = DB.execute("SELECT * FROM tag WHERE name = ?", (tag_name_1,))
        res = cursor.fetchall()
        tag_1 = Tag(name=res[0][1], id=res[0][0])

        cursor: Cursor = DB.execute("SELECT * FROM tag WHERE name = ?", (tag_name_2,))
        res = cursor.fetchall()
        tag_2 = Tag(name=res[0][1], id=res[0][0])

        cursor: Cursor = DB.execute("SELECT * FROM tag WHERE name = ?", (tag_name_3,))
        res = cursor.fetchall()
        tag_3 = Tag(name=res[0][1], id=res[0][0])

        return tag_name_1, tag_name_2, tag_name_3

    def clean_up(self, tag_name_1: str, tag_name_2: str, tag_name_3: str):
        DB.execute("DELETE FROM tag WHERE name = ?", (tag_name_1,))
        DB.execute("DELETE FROM tag WHERE name = ?", (tag_name_2,))
        DB.execute("DELETE FROM tag WHERE name = ?", (tag_name_3,))

    def test_save_and_get_all(self):
        DB.init()
        tag_name_1, tag_name_2, tag_name_3 = self.insert_seed_data()

        tag_1 = Tag(tag_name_1)
        tag_2 = Tag(tag_name_2)
        tag_3 = Tag(tag_name_3)

        # Save
        tag_1.save()
        tag_2.save()
        tag_3.save()

        # Get all
        tag_list = Tag.get_all()

        # Assert
        assert any([x.name == tag_name_1 for x in tag_list])
        assert any([x.name == tag_name_2 for x in tag_list])
        assert any([x.name == tag_name_3 for x in tag_list])

        # Clean up
        self.clean_up(tag_name_1, tag_name_2, tag_name_3)

    def test_edit(self):
        DB.init()
        tag_name_1, tag_name_2, tag_name_3 = self.insert_seed_data()

        tag_1 = Tag(tag_name_1)
        tag_2 = Tag(tag_name_2)
        tag_3 = Tag(tag_name_3)

        # Save
        tag_1.save()
        tag_2.save()
        tag_3.save()

        tag_1.name = "tag1"
        tag_1.update()
        tag_2.name = "tag2"
        tag_2.update()
        tag_3.name = "tag3"
        tag_3.update()

        # Get all
        tag_list = Tag.get_all()

        assert any([x.name == "tag1" for x in tag_list])
        assert any([x.name == "tag2" for x in tag_list])
        assert any([x.name == "tag3" for x in tag_list])

        # Clean up
        self.clean_up(tag_name_1, tag_name_2, tag_name_3)

    def test_delete(self):
        DB.init()
        tag_name_1, tag_name_2, tag_name_3 = self.insert_seed_data()
        tag_1 = Tag(tag_name_1)
        tag_2 = Tag(tag_name_2)
        tag_3 = Tag(tag_name_3)
        tag_1.save()
        tag_2.save()
        tag_3.save()
        tag_1.delete()
        tag_2.delete()
        tag_3.delete()
        tag_list = Tag.get_all()

        assert any(
            [not ((x.name == tag_name_1) and (x.name == tag_name_2) and (x.name == tag_name_3)) for x in tag_list])
