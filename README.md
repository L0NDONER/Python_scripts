# Media Organizer

![Python](5848152fcef1014c0b5e4967.png)

## Overview
Media Organizer is a Python script that continuously monitors a specified directory for new media files and automatically categorizes them into appropriate folders. It uses the `watchdog` library to observe file system events and organizes media files based on predefined rules for TV shows, movies, and other file types.

## Features
- **Automatic File Categorization**: Classifies and moves media files to respective directories for TV shows, movies, etc.
- **Modular Design**: Follows the Open-Closed Principle, making the script extensible for new file types without modifying existing code.
- **Background Monitoring**: Uses `watchdog` to monitor a directory in real-time for new file additions.

## Requirements
- Python 3.x
- `watchdog` library (can be installed via `pip install watchdog`)

## Usage
1. **Set Up the Script**: Place the script in a suitable directory.
2. **Run the Script**: Use the command `python3 MediaOrganizer.py /path/to/watch/folder`. Replace `/path/to/watch/folder` with the path of the directory you want to monitor.
3. **Background Execution**: Optionally, run the script in the background using `nohup` or as a system service.

## Customization
- **FileProcessor Classes**: Extend or modify the `TVShowProcessor`, `MovieProcessor`, and `OtherProcessor` classes for custom file handling logic.
- **File Extension Filters**: Adjust the `ignored_extensions` in the `FileProcessor` class to ignore specific file types.

## Contributing
Contributions to enhance Media Organizer or add new features are welcome. Please follow standard coding conventions and add tests for new functionalities.

## License
[MIT License](LICENSE)

## Acknowledgements
- This project utilizes the [watchdog](https://pypi.org/project/watchdog/) library for monitoring file system events.

