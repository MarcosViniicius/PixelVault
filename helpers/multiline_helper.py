from rich.console import Console
console = Console()

def read_multiline(prompt="Paste your text. Type END on a new line to finish:\n"):
    console.print(f"\n{prompt}")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)
