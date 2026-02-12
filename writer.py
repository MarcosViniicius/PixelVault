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
from helpers.byte_converter_helper import file_to_base64

console = Console()


def hide_archive_in_image():
    """
    Hides a file inside PNG images using Base64 encoding and LSB steganography.
    Supports large files by splitting across multiple images.
    """
    console.print(
        Panel.fit(
            "[bold cyan]Hide File in Image (Base64)[/bold cyan]\n"
            "[dim]Hides any file inside PNG images using Base64 encoding.\nSupports large files with multiple images.[/dim]",
            border_style="cyan"
        )
    )

    # Check if input directory exists
    if not os.path.isdir(config.INPUT_FILES_DIR):
        console.print(f"[bold red]Input folder not found: {config.INPUT_FILES_DIR}[/bold red]")
        return
    
    # List all files in input directory
    all_files = [f for f in os.listdir(config.INPUT_FILES_DIR) 
                 if os.path.isfile(os.path.join(config.INPUT_FILES_DIR, f))]
    
    if not all_files:
        console.print(f"[bold yellow]No files found in {config.INPUT_FILES_DIR}[/bold yellow]")
        return
    
    # Display available files
    console.print("\n[bold]Available files:[/bold]\n")
    table = Table(show_header=False, box=None)
    for index, file in enumerate(all_files, start=1):
        file_path = os.path.join(config.INPUT_FILES_DIR, file)
        file_size = os.path.getsize(file_path)
        size_kb = file_size / 1024
        table.add_row(f"[bold green]{index}[/bold green]", file, f"[dim]{size_kb:.2f} KB[/dim]")
    console.print(table)
    
    # Get user selection
    choice = console.input("\n[bold yellow]Select the file number:[/bold yellow] ").strip()
    if not choice.isdigit():
        console.print("[bold red]Invalid input.[/bold red]")
        return
    
    choice = int(choice)
    if not (1 <= choice <= len(all_files)):
        console.print("[bold red]Invalid number.[/bold red]")
        return
    
    selected_file = all_files[choice - 1]
    path = os.path.join(config.INPUT_FILES_DIR, selected_file)
    
    console.print(f"\n[green]Selected:[/green] {selected_file}\n")
    
    # Get file name for metadata
    file_name = os.path.basename(path)
    
    # Ensure temporary folder exists
    os.makedirs(config.OUTPUT_TEMP_FILES, exist_ok=True)
    
    # Convert file to base64
    temp_payload_path = config.OUTPUT_TEMP_FILES + "temp_payload.txt"
    file_to_base64(path, temp_payload_path)
    
    # Read base64 content
    with open(temp_payload_path, 'r') as f:
        base64_content = f.read()
    
    # Create base image (can be the same dog image)
    if not os.path.exists(config.TEMP_IMAGE):
        console.print("[bold yellow]Base image not found. Creating a new one...[/bold yellow]")
        download_random_dog_image()
    
    # Calculate capacity and split base64 content if needed
    capacity = calculate_capacity(config.TEMP_IMAGE)
    overhead = calculate_overhead(file_name)
    max_payload_bytes = max(1, capacity - overhead)
    
    parts = split_text_by_bytes(base64_content, max_payload_bytes)
    total = len(parts)
    
    # Create output folder
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    folder_index = get_next_folder_index(config.OUTPUT_DIR)
    new_folder = os.path.join(config.OUTPUT_DIR, f"{config.FOLDER_ARCHIVES_PREFIX}{folder_index}")
    os.makedirs(new_folder, exist_ok=True)
    
    # Display information
    info = Table(show_header=False, box=None)
    info.add_row("[bold]File:[/bold]", f"[green]{file_name}[/green]")
    info.add_row("[bold]Output folder:[/bold]", f"[green]{new_folder}[/green]")
    info.add_row("[bold]Image capacity (approx):[/bold]", f"{capacity} bytes")
    info.add_row("[bold]Usable payload per image:[/bold]", f"{max_payload_bytes} bytes")
    info.add_row("[bold]Total base64 size:[/bold]", f"{len(base64_content)} bytes")
    info.add_row("[bold]Images to generate:[/bold]", str(total))
    console.print(info)
    console.print("")
    
    # Save base64 content to text file in base64 subfolder
    base64_folder = os.path.join(new_folder, "base64")
    os.makedirs(base64_folder, exist_ok=True)
    base64_txt_path = os.path.join(base64_folder, "payload.txt")
    
    with open(base64_txt_path, 'w') as f:
        f.write(base64_content)
    
    console.print(f"[dim]Base64 text file saved: {base64_txt_path}[/dim]\n")
    
    # Hide base64 into images with progress bar
    with Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("Hiding file into images...", total=total)
        
        for i, chunk in enumerate(parts, start=1):
            output_name = os.path.join(new_folder, f"{i}{config.OUTPUT_SUFFIX}")
            
            payload = {
                "filename": file_name,
                "part": i,
                "total": total,
                "data": chunk
            }
            
            secret_data = json.dumps(payload, ensure_ascii=False)
            secret_img = lsb.hide(config.TEMP_IMAGE, secret_data)
            secret_img.save(output_name)
            
            progress.advance(task)
    
    # Delete temporary base64 file after hiding in image
    try:
        os.remove(temp_payload_path)
    except Exception:
        pass
    
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
