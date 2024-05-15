import pytest
from src.database.seed import Seeder
import os

'''
To seed the database, and used by the test functions
This will clear the database anyway! 
-@ganadipa
'''
@pytest.fixture(scope="module")
def seeder():
    seeder = Seeder()
    seeder.seed()
    yield seeder
    seeder.clear()

def test_database_files_exist(seeder):
    assert os.path.exists(seeder.db_path), "Database path does not exist"
    assert os.path.exists(seeder.image_folder_path), "Image folder path does not exist"

def test_cloth_data(seeder):
    cloth_data = seeder.fetch_data('cloth')

    # Why overalls? absolutely random when choosing one of the cloths name.
    assert any('overalls' in item[1] for item in cloth_data), "No 'overalls' in cloth data"

def test_tag_data(seeder):
    tag_data = seeder.fetch_data('tag')

    # Why Casual? absolutely random when choosing one of the tags name.
    assert any('Casual' in item[1] for item in tag_data), "No 'Casual' tag found"

def test_outfit_data(seeder):
    outfit_data = seeder.fetch_data('outfit')

    # Why Casual Outfit? absolutely random when choosing one of the outfits name.
    assert any('Casual Outfit' in item[1] for item in outfit_data), "No 'Casual Outfit' found"

def test_cloth_tag_relations(seeder):
    cloth_tag_data = seeder.fetch_data('cloth_tag')

    # Why this magic number? it is generated while seeding, so if this assert fails, then seeding is actually broken.
    assert any(item[1] == 0 and item[2] == 0 for item in cloth_tag_data), "Mismatch in cloth_tag relations"

def test_outfit_cloth_relations(seeder):
    outfit_cloth_data = seeder.fetch_data('outfit_cloth')

    # Why this magic number? it is generated while seeding, so if this assert fails, then seeding is actually broken.
    assert any(item[1] == 0 and item[2] == 0 for item in outfit_cloth_data), "Mismatch in outfit_cloth relations"

def test_clear_data(seeder):
    seeder.clear()
    assert len(seeder.fetch_data('cloth')) == 0, "Cloth data not cleared"
    assert len(seeder.fetch_data('tag')) == 0, "Tag data not cleared"
    assert len(seeder.fetch_data('outfit')) == 0, "Outfit data not cleared"
    assert len(seeder.fetch_data('cloth_tag')) == 0, "Cloth-tag data not cleared"
    assert len(seeder.fetch_data('outfit_cloth')) == 0, "Outfit-cloth data not cleared"
