import os

def damage_archive(archive_path):
   
    if not os.path.exists(archive_path):
        print(f"Archive patn {archive_path} not found.")
        return
    
    try:
        with open(archive_path, "ab") as f:
            f.write(b"corrupted_data")
        print(f"Archive {archive_path} was corrupted.")
    except Exception as e:
        print(f"Error at corrupten archive: {e}")

if __name__ == "__main__":
    ARCHIVE_PATH = "/home/zerg/out/arx2.7z"
    damage_archive(ARCHIVE_PATH)
