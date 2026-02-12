"""
Configuration constants for the Image Text Writer project.
"""

# Directories
OUTPUT_DIR = "./output"
TEMP_IMAGE = "image.png"

# API
DOG_API_URL = "https://dog.ceo/api/breeds/image/random"
API_TIMEOUT = 10

# Steganography settings
SAFETY_FACTOR = 0.75
OVERHEAD_BASE = 512

# File patterns
FILE_PATTERN = r"^(\d+)_output\.png$"
FOLDER_PREFIX = "text_"
OUTPUT_SUFFIX = "_output.png"
