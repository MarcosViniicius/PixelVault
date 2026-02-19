# multiline_helper.py - Helper function to read multiline user input until 'END' is typed.
from rich.console import Console
console = Console()

# Reads multiline user input via console until 'END' is typed and returns the combined text.
def read_multiline(prompt="Paste your text. Type END on a new line to finish:\n"):
    console.print(f"\n{prompt}")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)
