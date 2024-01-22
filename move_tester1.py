#!/usr/bin/env python3

import os
import sys
import time
import re
from abc import ABC, abstractmethod
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileCategorizer(ABC):
    @abstractmethod
    def categorize(self, file_path):
        pass


class TvShowCategorizer(FileCategorizer):
    def categorize(self, file_path):
        file_name = os.path.basename(file_path)
        tv_show_pattern = re.compile(r'S\d{2}E\d{2}', re.IGNORECASE)
        return bool(tv_show_pattern.search(file_name))


class MovieCategorizer(FileCategorizer):
    def __init__(self):
        self.movie_keywords = [
            '720p',
            '1080p',
            'bluray',
            'webrip',
            'dvdrip',
            '.ssr']

    def categorize(self, file_path):
        file_name = os.path.basename(file_path)
        lowercase_file_name = file_name.lower()
        return any(
            keyword in lowercase_file_name for keyword in self.movie_keywords)


class DownloadHandler(FileSystemEventHandler):
    def __init__(self, categorizers):
        self.categorizers = categorizers

    def on_created(self, event):
        if event.is_directory:
            return
        self.process_file(event.src_path)

    def process_file(self, file_path):
        for categorizer in self.categorizers:
            if categorizer.categorize(file_path):
                category = categorizer.__class__.__name__
                destination_folder = os.path.join(
                    self.destination_folder, category)
                self.move_file(file_path, destination_folder)
                return  # Stop after the first categorizer matches

    def move_file(self, file_path, destination_folder):
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(destination_folder, file_name)
        try:
            os.rename(file_path, destination_path)
            print(f"Moved {file_name} to {destination_path}")
        except Exception as e:
            print(f"Error moving {file_name}: {e}")

    def process_existing_files(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                self.process_file(os.path.join(root, file_name))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/folder")
        sys.exit(1)

    destination_folder = '/media'
    watch_folder = os.path.abspath(sys.argv[1])

    tv_show_categorizer = TvShowCategorizer()
    movie_categorizer = MovieCategorizer()

    event_handler = DownloadHandler(
        categorizers=[
            tv_show_categorizer,
            movie_categorizer])
    observer = Observer()

    event_handler.watch_folder = watch_folder
    event_handler.destination_folder = destination_folder

    observer.schedule(event_handler, watch_folder, recursive=True)

    print(f"Watching {watch_folder} for new downloads...")

    event_handler.process_existing_files(watch_folder)

    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
