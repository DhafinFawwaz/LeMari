from sqlite3 import *
import secrets
from typing import List
from flet_core.file_picker import FilePickerFile
from typing import Tuple

from src.database.database import DB
from src.database.cloth import Cloth
from src.database.tag import Tag


class TestCloth:

    def insert_seed_data(self) -> Tuple[str, str, str, Tag, Tag, Tag]:
        prefix_1 = secrets.token_hex(8)
        prefix_2 = secrets.token_hex(8)
        prefix_3 = secrets.token_hex(8)
        
        tag_name_1 = secrets.token_hex(8)
        tag_name_2 = secrets.token_hex(8)
        tag_name_3 = secrets.token_hex(8)

        DB.execute(f"INSERT INTO tag (name) VALUES (?), (?), (?)", (tag_name_1, tag_name_2, tag_name_3))
        cursor: Cursor = DB.execute(f"SELECT * FROM tag WHERE name = ?", (tag_name_1,))
        res = cursor.fetchall()
        tag_1 = Tag(name=res[0][1], id=res[0][0])

        cursor: Cursor = DB.execute(f"SELECT * FROM tag WHERE name = ?", (tag_name_2,))
        res = cursor.fetchall()
        tag_2 = Tag(name=res[0][1], id=res[0][0])

        cursor: Cursor = DB.execute(f"SELECT * FROM tag WHERE name = ?", (tag_name_3,))
        res = cursor.fetchall()
        tag_3 = Tag(name=res[0][1], id=res[0][0])

        return prefix_1, prefix_2, prefix_3, tag_1, tag_2, tag_3
    
    def clean_up(self, prefix_1: str, prefix_2: str, prefix_3: str, tag_name_1: str, tag_name_2: str, tag_name_3: str):
        DB.execute("DELETE FROM cloth WHERE name = ?", (f'{prefix_1}',))
        DB.execute("DELETE FROM cloth WHERE name = ?", (f'{prefix_2}',))
        DB.execute("DELETE FROM cloth WHERE name = ?", (f'{prefix_3}',))
        
        DB.execute("DELETE FROM tag WHERE name = ?", (tag_name_1,))
        DB.execute("DELETE FROM tag WHERE name = ?", (tag_name_2,))
        DB.execute("DELETE FROM tag WHERE name = ?", (tag_name_3,))

    def test_save_and_get_all(self):
        DB.init()
        prefix_1, prefix_2, prefix_3, tag_1, tag_2, tag_3 = self.insert_seed_data()

        cloth_1 = Cloth(f'{prefix_1}', f'{prefix_1}.png', [tag_1, tag_3])
        cloth_2 = Cloth(f'{prefix_2}', f'{prefix_2}.png', [tag_1, tag_2, tag_3])
        cloth_3 = Cloth(f'{prefix_3}', f'{prefix_3}.png', [tag_2])

        # Save
        cloth_1.save()
        cloth_2.save()
        cloth_3.save()

        # Get all
        cloth_list = Cloth.get_all()

        # Assert
        assert any([x.name == f'{prefix_1}' and x.image_name == f'{prefix_1}.png' for x in cloth_list])
        assert any([x.name == f'{prefix_2}' and x.image_name == f'{prefix_2}.png' for x in cloth_list])
        assert any([x.name == f'{prefix_3}' and x.image_name == f'{prefix_3}.png' for x in cloth_list])
        
        # Clean up
        self.clean_up(prefix_1, prefix_2, prefix_3, tag_1.name, tag_2.name, tag_3.name)
        

    def test_find_all_by_search_and_tags(self):
        DB.init()
        prefix_1, prefix_2, prefix_3, tag_1, tag_2, tag_3 = self.insert_seed_data()

        cloth_1 = Cloth(f'{prefix_1}', f'{prefix_1}.png', [tag_1, tag_3])
        cloth_2 = Cloth(f'{prefix_2}', f'{prefix_2}.png', [tag_1, tag_2, tag_3])
        cloth_3 = Cloth(f'{prefix_3}', f'{prefix_3}.png', [tag_2])
        cloth_1.save()
        cloth_2.save()
        cloth_3.save()

        search_filter = ''
        tag_list_filter = [tag_1, tag_3]

        cloth_list: List[Cloth] = Cloth.find_all_by_search_and_tags(search_filter, tag_list_filter)


        # Assert
        # cloth_1 and cloth_2 should be in the list, but not cloth_3
        assert any([x.name == f'{prefix_1}' and x.image_name == f'{prefix_1}.png' for x in cloth_list])
        assert any([x.name == f'{prefix_2}' and x.image_name == f'{prefix_2}.png' for x in cloth_list])
        assert all([not (x.name == f'{prefix_3}' and x.image_name == f'{prefix_3}.png') for x in cloth_list])
        
        # Clean up
        self.clean_up(prefix_1, prefix_2, prefix_3, tag_1.name, tag_2.name, tag_3.name)
    
    def test_edit(self):
        DB.init()
        prefix_1, prefix_2, prefix_3, tag_1, tag_2, tag_3 = self.insert_seed_data()

        cloth_1 = Cloth(f'{prefix_1}', f'{prefix_1}.png', [tag_1, tag_3])
        cloth_2 = Cloth(f'{prefix_2}', f'{prefix_2}.png', [tag_1, tag_2, tag_3])
        cloth_3 = Cloth(f'{prefix_3}', f'{prefix_3}.png', [tag_2])
        cloth_1.save()
        cloth_2.save()
        cloth_3.save()

        # Edit
        cloth_1.name = f'{prefix_1}_edited'
        cloth_1.image_name = f'{prefix_1}_edited.png'
        cloth_1.tag_list = [tag_2]

        search_filter = ''
        tag_list_filter = [tag_1, tag_3]

        cloth_list: List[Cloth] = Cloth.find_all_by_search_and_tags(search_filter, tag_list_filter)

        # Assert
        # cloth_2 should be in the list, but not cloth_1 cloth_3
        assert any([x.name == f'{prefix_2}' and x.image_name == f'{prefix_2}.png' for x in cloth_list])
        assert all([not (x.name == f'{prefix_3}' and x.image_name == f'{prefix_3}.png') for x in cloth_list])
        assert all([not (x.name == f'{prefix_1}_edited' and x.image_name == f'{prefix_1}_edited.png') for x in cloth_list])
        
        # Clean up
        self.clean_up(prefix_1, prefix_2, prefix_3, tag_1.name, tag_2.name, tag_3.name)

    def test_delete(self):
        DB.init()
        prefix_1, prefix_2, prefix_3, tag_1, tag_2, tag_3 = self.insert_seed_data()

        cloth_1 = Cloth(f'{prefix_1}', f'{prefix_1}.png', [tag_1, tag_3])
        cloth_2 = Cloth(f'{prefix_2}', f'{prefix_2}.png', [tag_1, tag_2, tag_3])
        cloth_3 = Cloth(f'{prefix_3}', f'{prefix_3}.png', [tag_2])
        cloth_1.save()
        cloth_2.save()
        cloth_3.save()

        cloth_2.delete()

        search_filter = ''
        tag_list_filter = [tag_1, tag_2]
        cloth_list: List[Cloth] = Cloth.find_all_by_search_and_tags(search_filter, tag_list_filter)

        # Assert
        # cloth_2 shouldn't be in the list, but cloth_1 and cloth_3 exist
        assert any([x.name == f'{prefix_1}' and x.image_name == f'{prefix_1}.png' for x in cloth_list])
        assert any([x.name == f'{prefix_3}' and x.image_name == f'{prefix_3}.png' for x in cloth_list])
        assert all([not (x.name == f'{prefix_2}' and x.image_name == f'{prefix_2}.png') for x in cloth_list])
        
        # Clean up
        self.clean_up(prefix_1, prefix_2, prefix_3, tag_1.name, tag_2.name, tag_3.name)

