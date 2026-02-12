from reader import read_image
from writer import create_image, write_image
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich import print
from helpers.multiline_helper import read_multiline

console = Console()

def show_header():
    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan]Image Text Writer[/bold cyan]\n"
            "[dim]Read text from images or create new ones with custom metadata.[/dim]",
            border_style="cyan"
        )
    )

def show_menu():
    table = Table(show_header=False, box=None, pad_edge=False)
    table.add_row("[bold green]1[/bold green]", "Read text from an existing image")
    table.add_row("[bold green]2[/bold green]", "Create a new image and add text")
    table.add_row("[bold red]Enter[/bold red]", "Exit")
    console.print("\n[bold]Choose an option:[/bold]\n")
    console.print(table)

def main():
    while True:
        show_header()
        show_menu()

        option = console.input("\n[bold yellow]Your choice:[/bold yellow] ").strip()

        if option == "":
            console.print("\n[bold red]Program closed.[/bold red]")
            break

        if option == "1":
            console.print("\n[green]Reading image...[/green]")
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

            create_image()

            with console.status("[cyan]Writing images...[/cyan]"):
                write_image(title, comment)

            console.print("\n[bold green]Done![/bold green]")
            console.input("\n[dim]Press Enter to return to the menu...[/dim]")
            continue

        console.print("\n[bold red]Invalid option. Try again.[/bold red]")
        console.input("\n[dim]Press Enter to continue...[/dim]")

if __name__ == "__main__":
    main()
