import os
import subprocess
import shutil

def get_image_dimensions(filepath):
    """Use ffprobe to get width and height of an image."""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=s=x:p=0', filepath
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        print(f"Error reading {filepath}: {result.stderr}")
        return None, None

    try:
        width, height = map(int, result.stdout.strip().split('x'))
        return width, height
    except ValueError:
        print(f"Unexpected ffprobe output for {filepath}: {result.stdout}")
        return None, None

def sort_images_by_orientation(folder_path):
    horizontal_folder = os.path.join(folder_path, 'horizontal')
    vertical_folder = os.path.join(folder_path, 'vertical')

    os.makedirs(horizontal_folder, exist_ok=True)
    os.makedirs(vertical_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if not os.path.isfile(file_path):
            continue  # skip folders

        width, height = get_image_dimensions(file_path)
        if width is None or height is None:
            continue  # skip unreadable files

        if width > height:
            shutil.move(file_path, os.path.join(horizontal_folder, filename))
            print(f"Moved {filename} to horizontal/")
        elif height > width:
            shutil.move(file_path, os.path.join(vertical_folder, filename))
            print(f"Moved {filename} to vertical/")
        else:
            print(f"{filename} is square, skipping.")

if __name__ == "__main__":
    folder = input("Enter the folder path: ").strip()
    sort_images_by_orientation(folder)
    print("Sorting completed.")