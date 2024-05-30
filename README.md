# SEARCH 🔎

This Python script allows you to search for files on your system with various filters and copy them automatically to a folder created on the desktop. It is designed to function similarly to the `find` command in Linux.

## Features 🩻

- Filter files by type (image, video, document, audio, archive, server)
- Filter files by extension
- Filter files by name
- Filter files by modification date (last 24 hours, last month, last year)
- Filter files by size
- Filter files by permissions
- Search recursively or non-recursively
- Copy the found files to an automatically created folder on the desktop

## Usage ⚙️

### Usage Examples:

- Search for all files in the current path:
  ```sh
  python3 search.py .
  ```

- Search for all PDF files in the current path:
  ```sh
  python3 search.py . -e .pdf
  ```

- Search for all image files in the current path:
  ```sh
  python3 search.py . -t image
  ```

- Search for all image files modified in the last 24 hours:
  ```sh
  python3 search.py . -t image -f 24h
  ```

- Search for all files containing "report" in the name:
  ```sh
  python3 search.py . -n report
  ```

- Search for all video files non-recursively:
  ```sh
  python3 search.py . -t video -r
  ```

- Search for all server configuration files in the current path:
  ```sh
  python3 search.py . -t server
  ```

## Options 🔤

- `--file-type` (`-t`): Filter by file type (e.g., image, video, document, audio, archive, server)
- `--extension` (`-e`): Filter files by extension (e.g., `.txt`, `.pdf`)
- `--name` (`-n`): Filter files by name (e.g., "report")
- `--no-recursive` (`-r`): Search non-recursively in directories (default is recursive)
- `--date-filter` (`-f`): Filter files by modification date (24h, month, year)

## Installation 📦

1. Clone the repository:
   ```sh
   git clone https://github.com/mgxy0/search.git
   ```
2. Navigate to the repository directory:
   ```sh
   cd search
   ```
3. Run the script:
   ```sh
   python search.py [options]
   ```

## Requirements 🗃️

- Python 3.x 🐍

## License 📄

GNU GPLv3 🐃

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### 2024 - mgxy0 / mark1n0
