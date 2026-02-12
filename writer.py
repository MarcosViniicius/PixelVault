import os
import json
from stegano import lsb
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn

import config
from helpers.image_helper import download_random_dog_image, calculate_capacity
from helpers.text_helper import split_text_by_bytes, calculate_overhead
from helpers.file_helper import get_next_folder_index

console = Console()


def write_image(title: str, comment: str):
    """
    Hides text within PNG images using LSB steganography.
    
    Args:
        title: Title of the hidden message
        comment: Text content to hide
    """
    if comment.strip() == "":
        console.print("[bold red]No text entered.[/bold red]")
        return

    console.print(
        Panel.fit(
            "[bold cyan]Image Writer (Steganography)[/bold cyan]\n"
            "[dim]Hides text inside PNG images using LSB (stegano).[/dim]",
            border_style="cyan"
        )
    )

    # Ensure output base folder exists
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)

    # Create next folder: text_1, text_2, text_3...
    folder_index = get_next_folder_index(config.OUTPUT_DIR)
    new_folder = os.path.join(config.OUTPUT_DIR, f"{config.FOLDER_PREFIX}{folder_index}")
    os.makedirs(new_folder)

    # Ensure base image exists
    if not os.path.exists(config.TEMP_IMAGE):
        console.print("[bold yellow]Base image not found. Creating a new one...[/bold yellow]")
        download_random_dog_image()

    # Calculate capacity and split text
    capacity = calculate_capacity(config.TEMP_IMAGE)
    overhead = calculate_overhead(title)
    max_payload_bytes = max(1, capacity - overhead)

    parts = split_text_by_bytes(comment, max_payload_bytes)
    total = len(parts)

    # Display information
    info = Table(show_header=False, box=None)
    info.add_row("[bold]Output folder:[/bold]", f"[green]{new_folder}[/green]")
    info.add_row("[bold]Image capacity (approx):[/bold]", f"{capacity} bytes")
    info.add_row("[bold]Usable payload per image:[/bold]", f"{max_payload_bytes} bytes")
    info.add_row("[bold]Total characters:[/bold]", str(len(comment)))
    info.add_row("[bold]Images to generate:[/bold]", str(total))
    console.print(info)
    console.print("")

    # Hide text into images with progress bar
    with Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console
    ) as progress:

        task = progress.add_task("Hiding text into images...", total=total)

        for i, chunk in enumerate(parts, start=1):
            output_name = os.path.join(new_folder, f"{i}{config.OUTPUT_SUFFIX}")

            payload = {
                "title": title,
                "part": i,
                "total": total,
                "text": chunk
            }

            secret_text = json.dumps(payload, ensure_ascii=False)
            secret_img = lsb.hide(config.TEMP_IMAGE, secret_text)
            secret_img.save(output_name)

            progress.advance(task)

    # Remove temporary base image
    try:
        os.remove(config.TEMP_IMAGE)
    except Exception:
        pass

    console.print(
        Panel(
            f"[bold green]Done![/bold green]\n"
            f"Generated [bold]{total}[/bold] image(s) in:\n[green]{new_folder}[/green]",
            border_style="green"
        )
    )
