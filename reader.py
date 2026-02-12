import os
import json
from stegano import lsb
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import config
from helpers.file_helper import list_folders, find_numbered_images

console = Console()

def read_image():
    """
    Reads and reconstructs hidden text from PNG images using LSB steganography.
    """
    console.print(
        Panel.fit(
            "[bold cyan]Image Reader (Steganography)[/bold cyan]\n"
            "[dim]Select a folder to reconstruct the full text hidden inside PNG images (LSB).[/dim]",
            border_style="cyan"
        )
    )

    # Check base folder
    if not os.path.isdir(config.OUTPUT_DIR):
        console.print("[bold red]Folder './output' not found.[/bold red]")
        return

    # Get folders
    folders = list_folders(config.OUTPUT_DIR)
    if not folders:
        console.print("[bold yellow]No folders found.[/bold yellow]")
        return

    # Display folders
    table = Table(show_header=False, box=None)
    for index, folder in enumerate(folders, start=1):
        table.add_row(f"[bold green]{index}[/bold green]", folder)

    console.print("\n[bold]Available folders:[/bold]\n")
    console.print(table)

    # Get user selection
    choice = console.input("\n[bold yellow]Select the folder number:[/bold yellow] ").strip()
    if not choice.isdigit():
        console.print("[bold red]Invalid input.[/bold red]")
        return

    choice = int(choice)
    if not (1 <= choice <= len(folders)):
        console.print("[bold red]Invalid number.[/bold red]")
        return

    selected_folder = folders[choice - 1]
    selected_path = os.path.join(config.OUTPUT_DIR, selected_folder)

    console.print(f"\n[green]Selected:[/green] {selected_folder}\n")

    # Find numbered images
    numbered_files = find_numbered_images(selected_path)

    if not numbered_files:
        console.print("[bold yellow]No output images found (e.g., 1_output.png, 2_output.png...).[/bold yellow]")
        return

    # Extract hidden text from images
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

                # Extract metadata and text
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

    # Rebuild text in correct order
    if expected_total is None:
        ordered_keys = sorted(parts.keys())
    else:
        ordered_keys = list(range(1, expected_total + 1))

    full_text = "".join(parts.get(k, "") for k in ordered_keys)

    # Show warnings for missing parts
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

    # Display extracted text
    console.print(
        Panel(
            f"[bold]Title:[/bold] {title if title else '(no title)'}\n\n"
            f"[bold]Text:[/bold]\n{full_text}",
            border_style="green"
        )
    )
