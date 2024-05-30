import os
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
    'document': ['open -a Preview', 'open -a Microsoft Word', 'open -a TextEdit'],
    'audio': ['open -a iTunes', 'open -a QuickTime Player', 'open -a Safari'],
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

def search_files(path, file_type=None, extension=None, name=None, recursive=True, date_filter=None):
    for root, dirs, files in os.walk(path):
        if not recursive:
            del dirs[:]
        
        dirs[:] = [d for d in dirs if not is_system_path(os.path.join(root, d))]

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
            
            print(file_path)
            open_file(file_path, file_type)

def main():
    parser = argparse.ArgumentParser(description="Find and open files similar to the Linux find command.")
    parser.add_argument("path", help="The directory path to start the search")
    parser.add_argument("-t", "--file-type", help="Filter by file type (e.g., image, video, document, audio, archive, server)")
    parser.add_argument("-e", "--extension", help="Filter files by extension")
    parser.add_argument("-n", "--name", help="Filter files by name")
    parser.add_argument("-r", "--no-recursive", help="Search non-recursively in directories", action="store_true", default=False)
    parser.add_argument("-f", "--date-filter", help="Filter files by modification date (24h, month, year)")

    args = parser.parse_args()
    
    search_files(
        args.path, file_type=args.file_type, extension=args.extension, name=args.name, recursive=not args.no_recursive, date_filter=args.date_filter
    )

if __name__ == "__main__":
    main()

