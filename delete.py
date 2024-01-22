#!/usr/bin/env python3

import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class PdfMoveHandler(FileSystemEventHandler):
    def __init__(self, source_folder, destination_folder):
        self.source_folder = source_folder
        self.destination_folder = destination_folder

    def on_created(self, event):
        if event.is_directory:
            return

        file_name = os.path.basename(event.src_path)
        if file_name.lower().endswith('.pdf'):
            move_pdf(self.source_folder, self.destination_folder, file_name)
            delete_remaining_pdfs(self.source_folder)


def move_pdf(source_folder, destination_folder, file_name):
    source_path = os.path.join(source_folder, file_name)
    destination_path = os.path.join(destination_folder, file_name)

    try:
        shutil.move(source_path, destination_path)
        print(f"Successfully moved {file_name} to {destination_folder}")
    except FileNotFoundError:
        print(f"File {file_name} not found in {source_folder}")
    except Exception as e:
        print(f"Error moving {file_name}: {e}")


def delete_remaining_pdfs(folder):
    for file_name in os.listdir(folder):
        if file_name.lower().endswith('.pdf'):
            file_path = os.path.join(folder, file_name)
            try:
                os.remove(file_path)
                print(f"Successfully deleted remaining PDF: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")


if __name__ == '__main__':
    source_folder = os.path.expanduser("~/Desktop")
    destination_folder = os.path.expanduser("~/media/Magazines")

    # Initial move for existing PDF files on Desktop
    for file_name in os.listdir(source_folder):
        if file_name.lower().endswith('.pdf'):
            move_pdf(source_folder, destination_folder, file_name)

    # Watch for future changes
    event_handler = PdfMoveHandler(source_folder, destination_folder)
    observer = Observer()
    observer.schedule(event_handler, path=source_folder, recursive=False)
    observer.start()

    try:
        print(f"Watching {source_folder} for PDF files. Press Ctrl+C to stop.")
        observer.join()
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
