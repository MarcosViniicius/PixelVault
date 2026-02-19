#config.py - Configuration constants for the Image Text Writer project.

# Directories
OUTPUT_TEMP_FILES = "./output/temp/"
OUTPUT_DIR = "./output"
INPUT_FILES_DIR = "./input/files"
TEMP_IMAGE = "./output/temp/image.png"

# API
DOG_API_URL = "https://dog.ceo/api/breeds/image/random"
API_TIMEOUT = 10

# Steganography settings
SAFETY_FACTOR = 0.75
OVERHEAD_BASE = 512

# File patterns
FILE_PATTERN = r"^(\d+)_output\.png$"
FOLDER_PREFIX = "text_"
FOLDER_ARCHIVES_PREFIX = "archive_"
OUTPUT_SUFFIX = "_output.png"
