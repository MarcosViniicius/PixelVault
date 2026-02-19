# text-helper.py - Helper functions for text manipulation.
import config


def split_text_by_bytes(text, max_bytes):
    # Splits text into UTF-8 chunks not exceeding max_bytes and returns the list of parts.
    if max_bytes <= 0:
        return []

    parts = []
    current_chars = []
    current_bytes = 0

    for char in text:
        char_bytes = len(char.encode("utf-8"))
        
        if current_bytes + char_bytes > max_bytes:
            # Save current part and start new one
            parts.append("".join(current_chars))
            current_chars = [char]
            current_bytes = char_bytes
        else:
            current_chars.append(char)
            current_bytes += char_bytes

    # Add remaining characters
    if current_chars:
        parts.append("".join(current_chars))

    return parts


def calculate_overhead(title):
    # Estimates JSON metadata overhead in bytes based on the provided title.
    return config.OVERHEAD_BASE + len(title.encode("utf-8"))
