import pytest
import os
from archive_utils import checkout
from damage_archive import damage_archive

# пути указаны как пример
ARCHIVE_PATH = "/home/zerg/out/arx2.7z"
EXTRACTED_FOLDER = "/home/zerg/folder1"
EXTRACTED_WITH_PATH_FOLDER = "/home/zerg/folder_with_paths"
BACKUP_ARCHIVE_PATH = "/home/zerg/out/arx2_backup.7z"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():

    if os.path.exists(ARCHIVE_PATH):
        if os.path.exists(BACKUP_ARCHIVE_PATH):
            os.remove(BACKUP_ARCHIVE_PATH)
        os.rename(ARCHIVE_PATH, BACKUP_ARCHIVE_PATH)
    
    if os.path.exists(BACKUP_ARCHIVE_PATH):
        os.rename(BACKUP_ARCHIVE_PATH, ARCHIVE_PATH)

    damage_archive(ARCHIVE_PATH)
    
    yield
    
    if os.path.exists(BACKUP_ARCHIVE_PATH):
        if os.path.exists(ARCHIVE_PATH):
            os.remove(ARCHIVE_PATH)
        os.rename(BACKUP_ARCHIVE_PATH, ARCHIVE_PATH)

def test_extract_damaged_archive():

    cmd = f"cd /home/zerg/out && 7z e arx2.7z -o{EXTRACTED_FOLDER} -y"
    assert not checkout(cmd, "Everything is Ok"), "test_extract_damaged_archive FAIL"

def test_test_damaged_archive():

    cmd = f"cd /home/zerg/out && 7z t arx2.7z"
    assert not checkout(cmd, "Everything is Ok"), "test_test_damaged_archive FAIL"
