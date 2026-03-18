import shutil
from pathlib import Path

# 1. Define your paths
# Use absolute paths to avoid ambiguity
source_dir = Path("Resources/ignored/nd/scikit-learn-mooc/figures")
module_root = Path("content/modules/M5")
target_dir = module_root / "assets"

# 2. List of filenames to recover
files_to_move = []



def restore_files():
    # Ensure the destination directory exists
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Error: Could not create directory {target_dir}: {e}")
        return

    print(f"Moving files from {source_dir} to {target_dir}...")

    for filename in files_to_move:
        source_path = source_dir / filename
        destination_path = target_dir / filename

        # Check if source file exists
        if source_path.exists() and source_path.is_file():
            try:
                # shutil.move handles cross-device moves (different partitions)
                shutil.move(str(source_path), str(destination_path))
                print(f"Successfully moved: {filename}")
            except Exception as e:
                print(f"Failed to move {filename}: {e}")
        else:
            print(f"Skipped: {filename} not found in source directory.")

if __name__ == "__main__":
    restore_files()