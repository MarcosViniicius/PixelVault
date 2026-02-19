# file_helper.py - Helper functions for file and folder operations.
    
import os
import re
import config


def list_folders(base_path):
    # Lists subdirectories in the given path and returns a sorted list of folder names.
    if not os.path.isdir(base_path):
        return []
    
    folders = [
        f for f in os.listdir(base_path) 
        if os.path.isdir(os.path.join(base_path, f))
    ]
    return sorted(folders)


def get_next_folder_index(base_path, prefix=config.FOLDER_PREFIX):
    # Returns the next available folder index based on the given base path and prefix.

    index = 1
    while os.path.isdir(os.path.join(base_path, f"{prefix}{index}")):
        index += 1
    return index


def find_numbered_images(folder_path, pattern=config.FILE_PATTERN):
    # Finds numbered output images in a folder and returns a sorted list of (number, filename).
    if not os.path.isdir(folder_path):
        return []
    
    regex = re.compile(pattern, re.IGNORECASE)
    numbered_files = []
    
    for filename in os.listdir(folder_path):
        match = regex.match(filename)
        if match:
            file_number = int(match.group(1))
            numbered_files.append((file_number, filename))
    
    return sorted(numbered_files, key=lambda x: x[0])
