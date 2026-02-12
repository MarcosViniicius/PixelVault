from PIL import Image
import random
import time
import os
import json

from stegano import lsb
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from io import BytesIO
import requests

console = Console()

def create_image(output_name="image.png"):
    try:
        # 1️⃣ Get random dog image URL
        api_url = "https://dog.ceo/api/breeds/image/random"
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        image_url = response.json()["message"]

        # 2️⃣ Download image bytes
        img_response = requests.get(image_url, timeout=15)
        img_response.raise_for_status()

        # 3️⃣ Open image from memory
        img = Image.open(BytesIO(img_response.content))

        # 4️⃣ Convert to RGB (important for PNG + steganography consistency)
        img = img.convert("RGB")

        # 5️⃣ Save as PNG
        img.save(output_name, format="PNG")

        print(f"Image downloaded and saved as '{output_name}'")

    except Exception as e:
        print(f"Error downloading image: {e}")



def _approx_capacity_bytes(image_path: str, safety: float = 0.75) -> int:
    """Capacidade aproximada de bytes para LSB 1-bit/canal (RGB), com margem de segurança."""
    with Image.open(image_path) as img:
        w, h = img.size
        raw = (w * h * 3) // 8  # bytes teóricos
        usable = int(raw * safety)
        return max(0, usable)


def _split_text_by_max_bytes(text: str, max_bytes: int) -> list[str]:
    """Divide texto garantindo que cada parte <= max_bytes em UTF-8."""
    if max_bytes <= 0:
        return []

    parts = []
    current = []
    current_bytes = 0

    for ch in text:
        b = len(ch.encode("utf-8"))
        if current_bytes + b > max_bytes:
            parts.append("".join(current))
            current = [ch]
            current_bytes = b
        else:
            current.append(ch)
            current_bytes += b

    if current:
        parts.append("".join(current))

    return parts


def write_image(title: str, comment: str):
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
    base_path = "./output"
    os.makedirs(base_path, exist_ok=True)

    # Create next folder: text_1, text_2, text_3...
    folder_index = 1
    while os.path.isdir(os.path.join(base_path, f"text_{folder_index}")):
        folder_index += 1

    new_folder = os.path.join(base_path, f"text_{folder_index}")
    os.makedirs(new_folder)

    # Ensure base image exists
    if not os.path.exists("image.png"):
        console.print("[bold yellow]Base image not found. Creating a new one...[/bold yellow]")
        create_image()

    capacity = _approx_capacity_bytes("image.png", safety=0.75)

    # Reservar espaço para cabeçalho JSON (title/part/total) + folga
    # (quanto maior o título, mais overhead)
    overhead_estimate = 512 + len(title.encode("utf-8"))
    max_payload_bytes = max(1, capacity - overhead_estimate)

    parts = _split_text_by_max_bytes(comment, max_payload_bytes)
    total = len(parts)

    info = Table(show_header=False, box=None)
    info.add_row("[bold]Output folder:[/bold]", f"[green]{new_folder}[/green]")
    info.add_row("[bold]Image capacity (approx):[/bold]", f"{capacity} bytes")
    info.add_row("[bold]Usable payload per image:[/bold]", f"{max_payload_bytes} bytes")
    info.add_row("[bold]Total characters:[/bold]", str(len(comment)))
    info.add_row("[bold]Images to generate:[/bold]", str(total))
    console.print(info)
    console.print("")

    with Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console
    ) as progress:

        task = progress.add_task("Hiding text into images...", total=total)

        for i, chunk in enumerate(parts, start=1):
            output_name = os.path.join(new_folder, f"{i}_output.png")

            payload = {
                "title": title,
                "part": i,
                "total": total,
                "text": chunk
            }

            secret_text = json.dumps(payload, ensure_ascii=False)

            # Hide into a fresh copy of the base image each time
            secret_img = lsb.hide("image.png", secret_text)
            secret_img.save(output_name)

            progress.advance(task)

    # Optional: remove base image
    try:
        os.remove("image.png")
    except Exception:
        pass

    console.print(
        Panel(
            f"[bold green]Done![/bold green]\n"
            f"Generated [bold]{total}[/bold] image(s) in:\n[green]{new_folder}[/green]",
            border_style="green"
        )
    )

    console.print("\n[dim]Returning to main menu...[/dim]")
    from main import main
    main()
