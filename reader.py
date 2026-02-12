import os
import json
from stegano import lsb
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import config
from helpers.file_helper import list_folders, find_numbered_images
from helpers.byte_converter_helper import base64_to_file

console = Console()


def extract_file_from_archive(folder_path: str):
    """
    Extracts a hidden file from archive folder images.
    Supports files split across multiple images.
    """
    # Check if base64 text file exists
    base64_folder = os.path.join(folder_path, "base64")
    base64_txt_path = os.path.join(base64_folder, "payload.txt")
    
    has_base64_file = os.path.exists(base64_txt_path)
    
    # Ask user extraction method
    console.print("\n[bold]Select extraction method:[/bold]")
    console.print("[green]1[/green] - Extract file from images (LSB steganography)")
    if has_base64_file:
        console.print("[green]2[/green] - Convert from base64 text file (faster)")
    
    method = console.input("\n[bold yellow]Choose option:[/bold yellow] ").strip()
    
    # Option 2: Use base64 text file directly
    if method == "2" and has_base64_file:
        try:
            with open(base64_txt_path, 'r') as f:
                base64_content = f.read()
            
            # Save to temporary file and convert
            os.makedirs(config.OUTPUT_TEMP_FILES, exist_ok=True)
            temp_file = os.path.join(config.OUTPUT_TEMP_FILES, "extracted_payload.txt")
            
            with open(temp_file, 'w') as f:
                f.write(base64_content)
            
            # Convert base64 back to original file
            output_name = os.path.join(folder_path, "extracted_file")
            base64_to_file(temp_file, output_name)
            
            # Clean up
            os.remove(temp_file)
            
            console.print(
                Panel(
                    f"[bold green]Success![/bold green]\n"
                    f"File extracted from base64 text file\n"
                    f"Saved in: [green]{folder_path}[/green]",
                    border_style="green"
                )
            )
            return
            
        except Exception as e:
            console.print(f"[bold red]Error: {e}[/bold red]")
            return
    
    # Option 1 or fallback: Extract from images
    # Find numbered images
    numbered_files = find_numbered_images(folder_path)
    
    if not numbered_files:
        console.print("[bold yellow]No output images found (e.g., 1_output.png, 2_output.png...).[/bold yellow]")
        return
    
    # Extract hidden data from images
    parts = {}
    filename = None
    expected_total = None
    errors = []
    
    with console.status("[cyan]Extracting hidden file...[/cyan]"):
        for idx, file in numbered_files:
            file_path = os.path.join(folder_path, file)
            
            try:
                secret = lsb.reveal(file_path)
                if not secret:
                    errors.append(f"{file}: no hidden data found")
                    continue
                
                data = json.loads(secret)
                
                # Extract metadata and base64 chunk
                part = int(data.get("part", idx))
                total = int(data.get("total", 0))
                chunk = data.get("data", "")
                
                if filename is None:
                    filename = data.get("filename", "extracted_file")
                
                if expected_total is None and total > 0:
                    expected_total = total
                
                parts[part] = chunk
                
            except Exception as e:
                errors.append(f"{file}: {e}")
    
    if not parts:
        console.print("[bold red]No readable hidden data was found in these images.[/bold red]")
        return
    
    # Rebuild base64 in correct order
    if expected_total is None:
        ordered_keys = sorted(parts.keys())
    else:
        ordered_keys = list(range(1, expected_total + 1))
    
    full_base64 = "".join(parts.get(k, "") for k in ordered_keys)
    
    # Show warnings for missing parts
    missing = []
    if expected_total is not None:
        missing = [k for k in range(1, expected_total + 1) if k not in parts]
    
    if missing:
        console.print(f"[bold yellow]Warning:[/bold yellow] Missing parts: {missing}")
        console.print("[bold red]File may be incomplete or corrupted![/bold red]")
    
    if errors:
        console.print("\n[bold yellow]Some files had issues:[/bold yellow]")
        for e in errors[:5]:
            console.print(f"- {e}")
        if len(errors) > 5:
            console.print(f"[dim]...and {len(errors) - 5} more[/dim]")
    
    # Save to temporary file and convert back to original file
    try:
        os.makedirs(config.OUTPUT_TEMP_FILES, exist_ok=True)
        temp_file = os.path.join(config.OUTPUT_TEMP_FILES, "extracted_payload.txt")
        
        with open(temp_file, 'w') as f:
            f.write(full_base64)
        
        # Convert base64 back to original file
        output_name = os.path.join(folder_path, "extracted_file")
        base64_to_file(temp_file, output_name)
        
        # Clean up temporary file
        os.remove(temp_file)
        
        console.print(
            Panel(
                f"[bold green]Success![/bold green]\n"
                f"File extracted: [bold]{filename}[/bold]\n"
                f"Saved in: [green]{folder_path}[/green]",
                border_style="green"
            )
        )
        
    except Exception as e:
        console.print(f"[bold red]Error converting file: {e}[/bold red]")


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

    # Ask user what type of operation to perform
    console.print("\n[bold]Select operation:[/bold]")
    console.print("[green]1[/green] - Read text from 'text_' folders")
    console.print("[green]2[/green] - Extract files from 'archive_' folders")
    
    operation = console.input("\n[bold yellow]Choose option (1 or 2):[/bold yellow] ").strip()
    
    if operation not in ["1", "2"]:
        console.print("[bold red]Invalid option.[/bold red]")
        return
    
    # Set folder prefix based on user choice
    if operation == "1":
        folder_prefix = config.FOLDER_PREFIX
    else:
        folder_prefix = config.FOLDER_ARCHIVES_PREFIX
    
    # Get folders filtered by prefix
    all_folders = list_folders(config.OUTPUT_DIR)
    folders = [f for f in all_folders if f.startswith(folder_prefix)]
    
    if not folders:
        console.print(f"[bold yellow]No '{folder_prefix}' folders found.[/bold yellow]")
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

    # Handle archive extraction (option 2)
    if operation == "2":
        extract_file_from_archive(selected_path)
        return

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
