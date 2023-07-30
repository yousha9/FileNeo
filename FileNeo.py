#! /usr/bin/python

#! /usr/bin/python3

import os
import sys
import requests

def show_help():
    print("Usage: python script_name.py [URL] [DESTINATION_PATH]")
    print("Example: python script_name.py https://example.com/file.txt ~/Downloads/file.txt")
    sys.exit(0)

def download_file_with_progress(url, local_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB
    progress_bar_width = 40

    try:
        with open(local_path, 'wb') as f:
            for data in response.iter_content(block_size):
                f.write(data)
                downloaded_size = min(os.path.getsize(local_path), total_size)
                progress = downloaded_size / total_size
                progress_bar = '#' * int(progress * progress_bar_width)
                spaces = ' ' * (progress_bar_width - len(progress_bar))
                print(f"\rDownloading: [{progress_bar}{spaces}] {progress * 100:.2f}% ", end='', flush=True)

        print("\nFile downloaded successfully.")
        print(f"File saved at: {local_path}")

    except Exception as e:
        print("\nError occurred while downloading the file:")
        print(f"Status Code: {response.status_code}")
        print(f"Reason: {response.reason}")
        print(f"Error message: {e}")

def replace_invalid_path_chars(path):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    return ''.join(c if c not in invalid_chars else '_' for c in path)

def get_downloads_folder():
    home_dir = os.path.expanduser("~")
    downloads_folder = os.path.join(home_dir, "Downloads")
    return downloads_folder

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1].lower() in ('-h', '--help'):
        show_help()
    
    if len(sys.argv) != 3:
        print("Invalid arguments. Use -h or --help for usage information.")
        sys.exit(1)

    url = sys.argv[1]
    destination_path = sys.argv[2]

    if not os.path.isabs(destination_path):
        # If the destination path is not absolute, use the "Downloads" folder in the user's home directory.
        downloads_folder = get_downloads_folder()
        destination_path = os.path.join(downloads_folder, destination_path)

    # Ensure the folder for the destination path exists.
    destination_folder = os.path.dirname(destination_path)
    os.makedirs(destination_folder, exist_ok=True)

    download_file_with_progress(url, destination_path)
