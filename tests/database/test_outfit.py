from sqlite3 import *
import secrets
from typing import List
from typing import Tuple

from src.database.database import DB
from src.database.cloth import Cloth
from src.database.tag import Tag
from src.database.outfit import Outfit

class TestOutfit:
    def insert_seed_data(self) -> Tuple[str, str, str, Cloth, Cloth, Cloth]:
        prefix_1 = secrets.token_hex(8)
        prefix_2 = secrets.token_hex(8)
        prefix_3 = secrets.token_hex(8)

        cloth_name_1 = secrets.token_hex(8)
        cloth_name_2 = secrets.token_hex(8)
        cloth_name_3 = secrets.token_hex(8)

        DB.execute(f"INSERT INTO cloth (name, image_name) VALUES (?, ?), (?, ?), (?, ?)", (cloth_name_1, f"{cloth_name_1}.png", cloth_name_2, f"{cloth_name_2}.png", cloth_name_3, f"{cloth_name_3}.png"))
        cursor: Cursor = DB.execute(f"SELECT * FROM cloth WHERE name = ?", (cloth_name_1,))
        res = cursor.fetchall()
        cloth_1 = Cloth(name=res[0][1], image_name=res[0][2], id=res[0][0])

        cursor: Cursor = DB.execute(f"SELECT * FROM cloth WHERE name = ?", (cloth_name_2,))
        res = cursor.fetchall()
        cloth_2 = Cloth(name=res[0][1], image_name=res[0][2], id=res[0][0])

        cursor: Cursor = DB.execute(f"SELECT * FROM cloth WHERE name = ?", (cloth_name_3,))
        res = cursor.fetchall()
        cloth_3 = Cloth(name=res[0][1], image_name=res[0][2], id=res[0][0])

        return prefix_1, prefix_2, prefix_3, cloth_1, cloth_2, cloth_3

    def clean_up(self, outfit_1: Outfit, outfit_2: Outfit, outfit_3: Outfit, cloth_1: Cloth, cloth_2: Cloth, cloth_3: Cloth):
        DB.execute("DELETE FROM outfit_cloth WHERE outfit_id = ?", (outfit_1.id,))
        DB.execute("DELETE FROM outfit WHERE id = ?", (outfit_1.id,))
        DB.execute("DELETE FROM outfit_cloth WHERE outfit_id = ?", (outfit_2.id,))
        DB.execute("DELETE FROM outfit WHERE id = ?", (outfit_2.id,))
        DB.execute("DELETE FROM outfit_cloth WHERE outfit_id = ?", (outfit_3.id,))
        DB.execute("DELETE FROM outfit WHERE id = ?", (outfit_3.id,))

        DB.execute("DELETE FROM cloth WHERE name = ?", (cloth_1.name,))
        DB.execute("DELETE FROM cloth WHERE name = ?", (cloth_2.name,))
        DB.execute("DELETE FROM cloth WHERE name = ?", (cloth_3.name,))

    def test_save_and_get_all(self):
        DB.init()
        prefix_1, prefix_2, prefix_3, cloth_1, cloth_2, cloth_3 = self.insert_seed_data()

        outfit_1 = Outfit(name=prefix_1, cloth_list=[cloth_1, cloth_3])
        outfit_2 = Outfit(name=prefix_2, cloth_list=[cloth_1, cloth_2, cloth_3])
        outfit_3 = Outfit(name=prefix_3, cloth_list=[cloth_2])

        # Save
        outfit_1.save()
        outfit_2.save()
        outfit_3.save()

        outfit_list = Outfit.get_all_outfit()

        # Assert
        assert any([x.name == f"{prefix_1}"] for x in outfit_list)
        assert any([x.name == f"{prefix_2}"] for x in outfit_list)
        assert any([x.name == f"{prefix_3}"] for x in outfit_list)

        self.clean_up(outfit_1, outfit_2, outfit_3, cloth_1, cloth_2, cloth_3)

    def test_edit(self):
        DB.init()
        prefix_1, prefix_2, prefix_3, cloth_1, cloth_2, cloth_3 = self.insert_seed_data()

        outfit_1 = Outfit(name=prefix_1, cloth_list=[cloth_1, cloth_3])
        outfit_2 = Outfit(name=prefix_2, cloth_list=[cloth_1, cloth_2, cloth_3])
        outfit_3 = Outfit(name=prefix_3, cloth_list=[cloth_2])
        outfit_1.save()
        outfit_2.save()
        outfit_3.save()

        outfit_1.name = f"{prefix_1}_edited_1"
        outfit_1.edit()
        outfit_2.name = f"{prefix_2}_edited_2"
        outfit_2.edit()
        outfit_3.name = f"{prefix_3}_edited_3"
        outfit_3.edit()

        outfit_list = Outfit.get_all_outfit()

        assert any([x.name == f"{prefix_1}_edited_1"] for x in outfit_list)
        assert any([x.name == f"{prefix_2}_edited_2"] for x in outfit_list)
        assert any([x.name == f"{prefix_3}_edited_3"] for x in outfit_list)

        self.clean_up(outfit_1, outfit_2, outfit_3, cloth_1, cloth_2, cloth_3)
    
    def test_delete(self):
        DB.init()
        prefix_1, prefix_2, prefix_3, cloth_1, cloth_2, cloth_3 = self.insert_seed_data()

        outfit_1 = Outfit(name=prefix_1, cloth_list=[cloth_1, cloth_3])
        outfit_2 = Outfit(name=prefix_2, cloth_list=[cloth_1, cloth_2, cloth_3])
        outfit_3 = Outfit(name=prefix_3, cloth_list=[cloth_2])
        outfit_1.save()
        outfit_2.save()
        outfit_3.save()

        outfit_2.delete()

        outfit_list = Outfit.get_all_outfit()

        assert any([x.name == f"{prefix_1}"] for x in outfit_list)
        assert any([x.name == f"{prefix_3}"] for x in outfit_list)
        assert all([x.name != f"{prefix_2}"] for x in outfit_list)

        self.clean_up(outfit_1, outfit_2, outfit_3, cloth_1, cloth_2, cloth_3)