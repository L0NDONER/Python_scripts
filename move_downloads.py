#!/usr/bin/env python3

# Import necessary libraries
import os
import sys
import time
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the file system event handler


class DownloadHandler(FileSystemEventHandler):
    # Method triggered on file creation
    def on_created(self, event):
        # Ignore if the event is for a directory
        if event.is_directory:
            return
        # Process the newly created file
        self.process_file(event.src_path)

    # Method to process a file
    def process_file(self, file_path):
        # Ignore if the file is not in the specified folder or has certain extensions
        if not file_path.startswith(self.watch_folder) or self.is_ignored_extension(file_path):
            return

        # Get the file name from the path
        file_name = os.path.basename(file_path)

        # Check if it's a TV show based on filename patterns
        tv_show_pattern = re.compile(r'S\d{2}E\d{2}', re.IGNORECASE)
        is_tv_show = bool(tv_show_pattern.search(file_name))

        # Define keywords for categorizing as Movies
        movie_keywords = ['720p', '1080p', 'bluray', 'webrip', 'dvdrip']

        # Determine the destination based on TV show or movie
        if is_tv_show:
            category = 'TV'
        elif any(keyword in file_name.lower() for keyword in movie_keywords):
            category = 'Movies'
        else:
            category = 'Other'
            return  # Skip processing for "Other" category

        # Move the file to the appropriate category
        destination_path = os.path.join(
            self.destination_folder, category, file_name)
        try:
            os.rename(file_path, destination_path)
            print(f"Moved {file_name} to {destination_path}")
        except Exception as e:
            print(f"Error moving {file_name}: {e}")

    # Method to check if a file has an ignored extension
    def is_ignored_extension(self, file_path):
        ignored_extensions = ['.jpeg', '.jpg', '.nfo']
        return any(file_path.lower().endswith(ext) for ext in ignored_extensions)

    # Method to process existing files in a folder
    def process_existing_files(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                self.process_file(os.path.join(root, file_name))


# Main block
if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/folder")
        sys.exit(1)

    # Set the destination folder
    destination_folder = '/media'

    # Initialize the event handler and observer
    event_handler = DownloadHandler()
    observer = Observer()

    # Get the folder path from the command-line argument
    watch_folder = os.path.abspath(sys.argv[1])
    event_handler.watch_folder = watch_folder
    event_handler.destination_folder = destination_folder

    # Schedule the event handler with the observer
    observer.schedule(event_handler, watch_folder, recursive=True)

    # Print a message indicating the start of the watching process
    print(f"Watching {watch_folder} for new downloads...")

    # Process existing files in the Downloads folder
    event_handler.process_existing_files(watch_folder)

    try:
        # Start the observer and keep it running
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the observer when a keyboard interrupt is received
        observer.stop()
    # Wait for the observer to finish
    observer.join()
