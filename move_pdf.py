#!/usr/bin/env python3

import os
import time
import shutil
from datetime import datetime


def move_media_files():
    """Continuously monitors ~/Downloads for movies and TV shows, moving them to /media,
    excluding specified extensions and ignoring dotfiles. Handles common media file patterns,
    logs successes and errors, and provides clear user-friendly output.

    Args:
        None

    Returns:
        None
    """

    source_dir = '~/Downloads'
    dest_dir = '/media'
    excluded_extensions = ('.nfo', '.jpeg', '.jpg',
                           '.sub', '.idx', '.torrent', '.png')
    ignore_dotfiles = True  # Set to True to exclude dotfiles like '.gitignore'

    while True:
        for filename in os.listdir(source_dir):
            file_path = os.path.join(source_dir, filename)

            if (
                ignore_dotfiles and os.path.basename(filename).startswith('.')
            ) or os.path.isdir(file_path):
                continue  # Skip dotfiles and directories

            _, extension = os.path.splitext(filename)
            extension = extension.lower()

            if extension not in excluded_extensions:
                try:
                    dest_path = get_destination_path(filename, dest_dir)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                    with open(dest_path, 'wb') as dest_file, open(file_path, 'rb') as src_file:
                        shutil.copyfileobj(src_file, dest_file)

                    # Move by copying and deleting for safety
                    os.remove(file_path)
                    log_success(filename, dest_path)
                except Exception as e:
                    log_error(filename, str(e))

        time.sleep(5)  # Check for new files every 5 seconds


def get_destination_path(filename, dest_dir):
    """Creates a destination path in /media/Movies or /media/TV based on filename patterns,
    ensuring correct placement without overwriting existing files.

    Args:
        filename: The name of the media file to be moved.
        dest_dir: The base directory where movies and TV folders will be created.

    Returns:
        The full path to the destination file.
    """

    base_dir = os.path.join(
        dest_dir, 'Movies' if 'movie' in filename.lower() else 'TV')
    file_root, _ = os.path.splitext(filename)  # Remove extension

    # Handle common media file patterns (example for seasons and episodes):
    if '1080p' in filename:
        file_root = f"{file_root} (1080p)"
    elif '720p' in filename:
        file_root = f"{file_root} (720p)"
    elif 'x265' in filename:
        file_root = f"{file_root} (x265)"
    elif 'season' in filename and 'episode' in filename:
        season_num = re.search(r'season(\d+)', filename).group(1)
        episode_num = re.search(r'episode(\d+)', filename).group(1)
        file_root = f"{file_root} - S{season_num}E{episode_num}"

    # Increment filename if the target file already exists (e.g., "Batman (2022).mkv", "Batman (2022) (2).mkv")
    i = 1
    while os.path.exists(os.path.join(base_dir, f"{file_root}{extension}")):
        file_root = f"{file_root} ({i})"
        i += 1

    return os.path.join(base_dir, f"{file_root}{extension}")


def log_success(filename, dest_path):
    """Logs a successful file move operation with a timestamp and user-friendly message."""

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{timestamp} | Successfully moved '{filename}' to '{dest_path}'")


def log_error(filename, error_msg):
    """Logs an error during a file move operation with a timestamp and detailed message."""

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{timestamp} | Error moving '{filename}': {error_msg}")
