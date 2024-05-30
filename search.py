import os
import shutil
import subprocess
import argparse
import time

FILE_TYPES = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'video': ['.mp4', '.avi', '.mov', '.mkv', '.flv'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx'],
    'audio': ['.mp3', '.wav', '.aac', '.flac'],
    'archive': ['.zip', '.rar', '.tar', '.gz'],
    'server': ['.conf', '.log', '.sh', '.service', '.env']
}

OPEN_PROGRAMS = {
    'image': ['open -a Preview', 'open -a Photos', 'open -a Safari'],
    'video': ['open -a QuickTime Player', 'open -a VLC', 'open -a Safari'],
    'document': ['open -a Preview', 'open -a Pages', 'open -a TextEdit'],
    'audio': ['open -a Music', 'open -a QuickTime Player', 'open -a Safari'],
    'archive': ['open -a Archive Utility', 'open -a The Unarchiver', 'open -a Safari'],
    'server': ['open -a TextEdit', 'open -a Visual Studio Code', 'open -a Terminal']
}

SYSTEM_DIRS = ['/System', '/Library', '/bin', '/sbin', '/usr']

def is_system_path(path):
    return any(path.startswith(system_dir) for system_dir in SYSTEM_DIRS)

def open_file(file_path, file_type):
    programs = OPEN_PROGRAMS.get(file_type, [])
    for program in programs:
        try:
            subprocess.run(f"{program} {file_path}", shell=True, check=True)
            break
        except subprocess.CalledProcessError:
            continue
    else:
        print(f"Could not open file {file_path} with available programs.")

def filter_by_date(file_path, date_filter):
    current_time = time.time()
    modification_time = os.path.getmtime(file_path)

    if date_filter == '24h':
        return current_time - modification_time <= 24 * 3600
    elif date_filter == 'month':
        return current_time - modification_time <= 30 * 24 * 3600
    elif date_filter == 'year':
        return current_time - modification_time <= 365 * 24 * 3600
    else:
        return True

def filter_by_size(file_path, size_filter):
    file_size = os.path.getsize(file_path)
    if size_filter.endswith('k'):
        size_filter = int(size_filter[:-1]) * 1024
    elif size_filter.endswith('m'):
        size_filter = int(size_filter[:-1]) * 1024 * 1024
    elif size_filter.endswith('g'):
        size_filter = int(size_filter[:-1]) * 1024 * 1024 * 1024
    else:
        size_filter = int(size_filter)
    
    return file_size <= size_filter

def filter_by_permissions(file_path, perm_filter):
    file_permissions = oct(os.stat(file_path).st_mode)[-3:]
    return file_permissions == perm_filter

def search_files(path, file_type=None, extension=None, name=None, date_filter=None, size_filter=None, perm_filter=None):
    found_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_system_path(file_path):
                continue

            if extension and not file.endswith(extension):
                continue
            
            if file_type and not any(file.endswith(ext) for ext in FILE_TYPES.get(file_type, [])):
                continue
            
            if name and name not in file:
                continue
            
            if date_filter and not filter_by_date(file_path, date_filter):
                continue

            if size_filter and not filter_by_size(file_path, size_filter):
                continue

            if perm_filter and not filter_by_permissions(file_path, perm_filter):
                continue
            
            found_files.append(file_path)
    
    return found_files

def create_desktop_folder(folder_name):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    target_folder = os.path.join(desktop_path, folder_name)
    os.makedirs(target_folder, exist_ok=True)
    return target_folder

def copy_files_to_folder(files, target_folder):
    for file in files:
        try:
            shutil.copy(file, target_folder)
            print(f"Copied {file} to {target_folder}")
        except Exception as e:
            print(f"Failed to copy {file} to {target_folder}: {e}")

def main():
    parser = argparse.ArgumentParser(description="SEARCH --- created by mgxy0 License: 2024 GNU GPLv3")
    parser.add_argument("path", help="The directory path to start the search")
    parser.add_argument("-t", "--file-type", help="Filter by file type (e.g., image, video, document, audio, archive, server)")
    parser.add_argument("-e", "--extension", help="Filter files by extension")
    parser.add_argument("-n", "--name", help="Filter files by name")
    parser.add_argument("-f", "--date-filter", help="Filter files by modification date (24h, month, year)")
    parser.add_argument("-s", "--size-filter", help="Filter files by size (e.g., 10k, 20m, 1g)")
    parser.add_argument("-p", "--perm-filter", help="Filter files by permissions (e.g., 755, 644)")

    args = parser.parse_args()
    
    found_files = search_files(
        args.path, file_type=args.file_type, extension=args.extension, name=args.name, date_filter=args.date_filter,
        size_filter=args.size_filter, perm_filter=args.perm_filter
    )

    if found_files:
        folder_name = "Found_Files"
        target_folder = create_desktop_folder(folder_name)
        copy_files_to_folder(found_files, target_folder)
        print(f"\nAll found files have been copied to: {target_folder}")
    else:
        print("No files found.")

if __name__ == "__main__":
    main()
