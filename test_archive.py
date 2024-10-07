import pytest
import os
import subprocess
from archive_utils import checkout
# пути указаны как пример
SOURCE_FOLDER = "/home/zerg/tst"
ARCHIVE_PATH = "/home/zerg/out/arx2.7z"
EXTRACTED_FOLDER = "/home/zerg/folder1"
EXTRACTED_WITH_PATH_FOLDER = "/home/zerg/folder_with_paths"

FILES_TO_ARCHIVE = ["file1.txt", "file2.txt", "file3.txt"]
EXTRACTED_FILES = ["file1.txt", "file2.txt", "file3.txt"]

@pytest.fixture(scope="module", autouse=True)
def setup_files():
    
    os.makedirs(SOURCE_FOLDER, exist_ok=True)
    os.makedirs(EXTRACTED_FOLDER, exist_ok=True)
    os.makedirs(EXTRACTED_WITH_PATH_FOLDER, exist_ok=True)
    
    for file in FILES_TO_ARCHIVE:
        file_path = os.path.join(SOURCE_FOLDER, file)
        with open(file_path, "w") as f:
            f.write(f"Содержимое {file}")
    
    yield
    
    for file in FILES_TO_ARCHIVE:
        file_path = os.path.join(SOURCE_FOLDER, file)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    for file in EXTRACTED_FILES:
        extracted_file_path = os.path.join(EXTRACTED_FOLDER, file)
        if os.path.exists(extracted_file_path):
            os.remove(extracted_file_path)
        extracted_with_path_file = os.path.join(EXTRACTED_WITH_PATH_FOLDER, file)
        if os.path.exists(extracted_with_path_file):
            os.remove(extracted_with_path_file)
    
    if os.path.exists(ARCHIVE_PATH):
        os.remove(ARCHIVE_PATH)

def test_create_archive():
    
    cmd = f"cd {SOURCE_FOLDER} && 7z a {ARCHIVE_PATH} " + " ".join(FILES_TO_ARCHIVE)
    assert checkout(cmd, "Everything is Ok"), "test_create_archive FAIL: Archive not success"

    assert os.path.exists(ARCHIVE_PATH), f"test_create_archive FAIL: Archive {ARCHIVE_PATH} not found."

def test_extract_archive():

    cmd = f"cd /home/zerg/out && 7z e arx2.7z -o{EXTRACTED_FOLDER} -y"
    assert checkout(cmd, "Everything is Ok"), "test_extract_archive FAIL: Unpack fail."

    for file in EXTRACTED_FILES:
        extracted_file_path = os.path.join(EXTRACTED_FOLDER, file)
        assert os.path.exists(extracted_file_path), f"test_extract_archive FAIL: Archive file {extracted_file_path} not found ."

def test_test_archive():
    
    cmd = f"cd /home/zerg/out && 7z t arx2.7z"
    assert checkout(cmd, "Everything is Ok"), "test_test_archive FAIL: Check archive fail."

def test_delete_from_archive():
   
    file_to_delete = "file_to_delete.txt"
    file_path = os.path.join(SOURCE_FOLDER, file_to_delete)
    
    with open(file_path, "w") as f:
        f.write("Contents file to be deleted.")
    
    cmd_add = f"cd {SOURCE_FOLDER} && 7z a {ARCHIVE_PATH} {file_to_delete}"
    assert checkout(cmd_add, "Everything is Ok"), "test_delete_from_archive FAIL: Add file to archive fail"
    
    cmd = f"cd /home/zerg/out && 7z d arx2.7z {file_to_delete}"
    assert checkout(cmd, "Everything is Ok"), "test_delete_from_archive FAIL: Delete from archive failed"

def test_update_archive():


    file_to_update = "file_to_update.txt"
    file_path = os.path.join(SOURCE_FOLDER, file_to_update)
    
    with open(file_path, "w") as f:
        f.write("New content file to update.")
    
    cmd = f"cd {SOURCE_FOLDER} && 7z u {ARCHIVE_PATH} {file_to_update}"
    assert checkout(cmd, "Everything is Ok"), "test_update_archive FAIL: Update archive fail"

def test_list_archive():

    cmd = f"cd /home/zerg/out && 7z l arx2.7z"
    assert checkout(cmd, "Everything is Ok"), "test_list_archive FAIL: Command 'l' not success"

    result = subprocess.run(
        cmd, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        encoding="utf-8"
    )
    assert result.returncode == 0, "test_list_archive FAIL: Command 'l' fail."
    
    for file in FILES_TO_ARCHIVE:
        assert file in result.stdout, f"test_list_archive FAIL: File {file} not find list archive."

def test_extract_with_paths():

    cmd = f"cd /home/zerg/out && 7z x arx2.7z -o{EXTRACTED_WITH_PATH_FOLDER} -y"

    assert checkout(cmd, "Everything is Ok"), "test_extract_with_paths FAIL: Extract with paths fail."

    for file in EXTRACTED_FILES:
        extracted_file_path = os.path.join(EXTRACTED_WITH_PATH_FOLDER, file)
        assert os.path.exists(extracted_file_path), f"test_extract_with_paths FAIL: File {extracted_file_path} not found after extracting paths."

def test_hash_archive():

    cmd_hash = f"cd /home/zerg/out && 7z h arx2.7z"
    result_hash = subprocess.run(
        cmd_hash, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        encoding="utf-8"
    )
    assert result_hash.returncode == 0, "test_hash_archive FAIL: Command 'h' fail."


    hash_line = next((line for line in result_hash.stdout.splitlines() if "Hash =" in line), None)
    assert hash_line is not None, "test_hash_archive FAIL: Not find the hash string in the command output 'h'."
    
    hash_value_7z = hash_line.split("=")[1].strip()
    assert hash_value_7z, "test_hash_archive FAIL: Hash command 'h' empty."

    cmd_crc32 = f"crc32 {ARCHIVE_PATH}"
    result_crc32 = subprocess.run(
        cmd_crc32, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        encoding="utf-8"
    )
    assert result_crc32.returncode == 0, "test_hash_archive FAIL: Command 'crc32' fail"

    crc32_value = result_crc32.stdout.strip()
    assert crc32_value, "test_hash_archive FAIL: CRC32 command 'crc32' empty"

    assert hash_value_7z == crc32_value, f"test_hash_archive FAIL: Hash 'h' ({hash_value_7z}) not match with CRC32 ({crc32_value})."
