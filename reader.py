import os
import re
import json
from stegano import lsb

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def read_image():
    base_path = "./output"

    console.print(
        Panel.fit(
            "[bold cyan]Image Reader (Steganography)[/bold cyan]\n"
            "[dim]Select a folder to reconstruct the full text hidden inside PNG images (LSB).[/dim]",
            border_style="cyan"
        )
    )

    # Check base folder
    if not os.path.isdir(base_path):
        console.print("[bold red]Folder './output' not found.[/bold red]")
        return

    # Get only folders
    folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    if not folders:
        console.print("[bold yellow]No folders found.[/bold yellow]")
        return

    # Display folders
    table = Table(show_header=False, box=None)
    for index, folder in enumerate(sorted(folders), start=1):
        table.add_row(f"[bold green]{index}[/bold green]", folder)

    console.print("\n[bold]Available folders:[/bold]\n")
    console.print(table)

    choice = console.input("\n[bold yellow]Select the folder number:[/bold yellow] ").strip()
    if not choice.isdigit():
        console.print("[bold red]Invalid input.[/bold red]")
        return

    choice = int(choice)
    if not (1 <= choice <= len(folders)):
        console.print("[bold red]Invalid number.[/bold red]")
        return

    selected_folder = sorted(folders)[choice - 1]
    selected_path = os.path.join(base_path, selected_folder)

    console.print(f"\n[green]Selected:[/green] {selected_folder}\n")

    # Match files like 1_output.png, 2_output.png...
    pattern = re.compile(r"^(\d+)_output\.png$", re.IGNORECASE)

    numbered_files = []
    for name in os.listdir(selected_path):
        m = pattern.match(name)
        if m:
            numbered_files.append((int(m.group(1)), name))

    numbered_files.sort(key=lambda x: x[0])

    if not numbered_files:
        console.print("[bold yellow]No output images found (e.g., 1_output.png, 2_output.png...).[/bold yellow]")
        return

    parts = {}
    title = None
    expected_total = None
    errors = []

    with console.status("[cyan]Revealing hidden text...[/cyan]"):
        for idx, filename in numbered_files:
            file_path = os.path.join(selected_path, filename)

            try:
                secret = lsb.reveal(file_path)
                if not secret:
                    errors.append(f"{filename}: no hidden data found")
                    continue

                data = json.loads(secret)

                # Basic validation
                part = int(data.get("part", idx))
                total = int(data.get("total", 0))
                text = data.get("text", "")

                if title is None:
                    title = data.get("title")

                if expected_total is None and total > 0:
                    expected_total = total

                parts[part] = text

            except Exception as e:
                errors.append(f"{filename}: {e}")

    if not parts:
        console.print("[bold red]No readable hidden text was found in these images.[/bold red]")
        return

    # Rebuild in correct order
    if expected_total is None:
        # fallback: use what we have
        ordered_keys = sorted(parts.keys())
    else:
        ordered_keys = list(range(1, expected_total + 1))

    full_text = "".join(parts.get(k, "") for k in ordered_keys)

    # Show warnings if some parts are missing
    missing = []
    if expected_total is not None:
        missing = [k for k in range(1, expected_total + 1) if k not in parts]

    if missing:
        console.print(f"[bold yellow]Warning:[/bold yellow] Missing parts: {missing}")

    if errors:
        console.print("\n[bold yellow]Some files had issues:[/bold yellow]")
        for e in errors[:8]:
            console.print(f"- {e}")
        if len(errors) > 8:
            console.print(f"[dim]...and {len(errors) - 8} more[/dim]")

    console.print(
        Panel(
            f"[bold]Title:[/bold] {title if title else '(no title)'}\n\n"
            f"[bold]Text:[/bold]\n{full_text}",
            border_style="green"
        )
    )

    console.print("\n[dim]Returning to main menu...[/dim]")
    from main import main
    main()
