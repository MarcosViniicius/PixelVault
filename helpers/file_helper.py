"""
Helper functions for file and folder operations.
"""
import os
import re
import config


def list_folders(base_path):
    """
    Lists all subdirectories in the given path.
    
    Args:
        base_path: Path to search for folders
        
    Returns:
        list: Sorted list of folder names
    """
    if not os.path.isdir(base_path):
        return []
    
    folders = [
        f for f in os.listdir(base_path) 
        if os.path.isdir(os.path.join(base_path, f))
    ]
    return sorted(folders)


def get_next_folder_index(base_path, prefix=config.FOLDER_PREFIX):
    """
    Finds the next available folder index (e.g., text_1, text_2, text_3...).
    
    Args:
        base_path: Base directory path
        prefix: Folder name prefix
        
    Returns:
        int: Next available index
    """
    index = 1
    while os.path.isdir(os.path.join(base_path, f"{prefix}{index}")):
        index += 1
    return index


def find_numbered_images(folder_path, pattern=config.FILE_PATTERN):
    """
    Finds all numbered output images in a folder (e.g., 1_output.png, 2_output.png).
    
    Args:
        folder_path: Path to the folder containing images
        pattern: Regex pattern to match filenames
        
    Returns:
        list: Sorted list of tuples (number, filename)
    """
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
