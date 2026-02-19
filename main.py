# main.py - Main entry point for the Image Steganography Tool.

from reader import read_image
from writer import write_image, hide_archive_in_image
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from helpers.multiline_helper import read_multiline
from helpers.file_structure_helper import create_directory_structure


console = Console()

def show_header():
    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan]Image Steganography Tool[/bold cyan]\n"
            "[dim]Hide and extract text or files within images using LSB steganography.[/dim]",
            border_style="cyan"
        )
    )

def show_menu():
    table = Table(show_header=False, box=None, pad_edge=False)
    table.add_row("[bold green]1[/bold green]", "Read text from images or extract hidden files")
    table.add_row("[bold green]2[/bold green]", "Create new images with hidden text")
    table.add_row("[bold green]3[/bold green]", "Hide a file inside images (supports large files)")
    table.add_row("[bold red]Enter[/bold red]", "Exit")
    console.print("\n[bold]Choose an option:[/bold]\n")
    console.print(table)

def main():
    create_directory_structure()
    while True:
        show_header()
        show_menu()

        option = console.input("\n[bold yellow]Your choice:[/bold yellow] ").strip()

        if option == "":
            console.print("\n[bold red]Program closed.[/bold red]")
            break

        if option == "1":
            console.print("\n[green]Reading images...[/green]")
            read_image()
            console.input("\n[dim]Press Enter to return to the menu...[/dim]")
            continue

        if option == "2":
            console.print("\n[cyan]Creating new image...[/cyan]")
            title = console.input("[bold]Enter the image title:[/bold] ").strip()

            comment = read_multiline(
                "Paste your text below. Type [bold]-- END --[/bold] on a new line to finish:"
            )

            if not comment.strip():
                console.print("\n[bold red]No text entered.[/bold red]")
                console.input("\n[dim]Press Enter to return to the menu...[/dim]")
                continue

            write_image(title, comment)

            console.input("\n[dim]Press Enter to return to the menu...[/dim]")
            continue
        if option == "3":
            console.print("\n[cyan]Hiding file in images...[/cyan]")
            hide_archive_in_image()
            console.input("\n[dim]Press Enter to return to the menu...[/dim]")
            continue

        console.print("\n[bold red]Invalid option. Try again.[/bold red]")
        console.input("\n[dim]Press Enter to continue...[/dim]")

if __name__ == "__main__":
    main()
