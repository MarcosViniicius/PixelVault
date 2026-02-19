# file_structure_helper.py - Helper functions to manage file and directory structure for the Image Steganography Tool.

import os
import config

OUTPUT_DIR = config.OUTPUT_DIR
OUTPUT_TEMP_FILES = config.OUTPUT_TEMP_FILES
INPUT_FILES_DIR = config.INPUT_FILES_DIR


def create_directory_structure():

    # Verify if the OUTPUT_DIR exists, if not create it
    if os.path.exists(OUTPUT_DIR):
        return
    else:
        os.makedirs(OUTPUT_DIR)
        print(f"Directory '{OUTPUT_DIR}' created.")

    # Verify if the OUTPUT_TEMP_FILE exists, if not create it
    if os.path.exists(OUTPUT_TEMP_FILES):
        return
    else:
        os.makedirs(OUTPUT_TEMP_FILES)
        print(f"Directory '{OUTPUT_TEMP_FILES}' created.")

    # Verify if the INPUT_FILES_DIR exists, if not create it
    if os.path.exists(INPUT_FILES_DIR):
        return
    else:
        os.makedirs(INPUT_FILES_DIR)
        print(f"Directory '{INPUT_FILES_DIR}' created.")