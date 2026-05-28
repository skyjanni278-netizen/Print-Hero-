from rich.console import Console
from rich.markup import escape

console = Console(highlight=False)


def clear_screen():
    console.clear()


def print_header(titel: str):
    console.print()
    console.rule(f"[bold cyan]{escape(str(titel))}[/bold cyan]", style="cyan")
    console.print()


def hp_bar(current: int, maximum: int, width: int = 16) -> str:
    """Rich-markup colored HP bar."""
    ratio  = max(0.0, current / maximum) if maximum > 0 else 0.0
    filled = int(ratio * width)
    bar    = "█" * filled + "░" * (width - filled)
    if ratio > 0.6:
        color = "green"
    elif ratio > 0.3:
        color = "yellow"
    else:
        color = "bold red"
    return f"[{color}]{bar}[/{color}]"


def energy_bar(current: int, maximum: int, width: int = 16) -> str:
    """Rich-markup colored energy bar."""
    ratio  = max(0.0, current / maximum) if maximum > 0 else 0.0
    filled = int(ratio * width)
    bar    = "█" * filled + "░" * (width - filled)
    return f"[blue]{bar}[/blue]"
