"""
Helper functions for text manipulation.
"""
import config


def split_text_by_bytes(text, max_bytes):
    """
    Splits text into chunks ensuring each part is <= max_bytes in UTF-8 encoding.
    
    Args:
        text: Text string to split
        max_bytes: Maximum bytes per chunk
        
    Returns:
        list: List of text chunks
    """
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
    """
    Calculates the overhead bytes needed for JSON metadata.
    
    Args:
        title: Title string
        
    Returns:
        int: Estimated overhead in bytes
    """
    return config.OVERHEAD_BASE + len(title.encode("utf-8"))
