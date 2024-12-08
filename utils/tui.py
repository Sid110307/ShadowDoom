from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table


class TUI:
    def __init__(self):
        self.console = Console()
        self.clear()

    def styled_print(self, message="", fore_color="default", back_color="default", style="normal", end="\n"):
        self.console.print(message, style = Style(color = fore_color, bgcolor = back_color, bold = (style == "bold")),
                           end = end)

    def decorative_header(self, text, width=60, fore_color="cyan"):
        self.console.print(Panel(text.center(width), style = fore_color, width = width))

    def section_title(self, text, width=60, fore_color="green"):
        self.console.print(f"\n{text.center(width)}", style = f"bold {fore_color}")
        self.console.print("─" * width, style = fore_color)

    def render_menu(self, options, width=60, fore_color="yellow"):
        table = Table(box = box.ROUNDED, show_header = False, width = width, style = fore_color)
        for i, option in enumerate(options, 1):
            table.add_row(f"{i}. {option}".ljust(width - 4))
        self.console.print(table)

    def key_value_display(self, items, align=False, width=60, fore_color="yellow"):
        table = Table(box = box.ROUNDED, show_header = False, width = width, style = fore_color)

        max_key_length = max(len(key) for key in items.keys() if key != "DIVIDER" and items[key] is not None)
        max_value_length = max(len(str(value)) for value in items.values() if value is not None)

        for key, value in items.items():
            if key == "DIVIDER":
                table.add_section()
            else:
                if align:
                    if value is None:
                        row_text = key.rjust(max_key_length)
                    else:
                        row_text = f"{key.rjust(max_key_length)}: {str(value).ljust(max_value_length)}"
                    row_text = row_text.center(width - 4)
                else:
                    row_text = f"{key}" if value is None else f"{key}: {value}"
                    row_text = row_text.ljust(width - 4)

                table.add_row(row_text)
        self.console.print(table)

    def list_display(self, items, center=False, width=60, fore_color="yellow"):
        table = Table(box = box.ROUNDED, show_header = False, width = width, style = fore_color)
        for item in items:
            row_text = " | ".join([f"{key}: {value}" for key, value in item.items()])
            row_text = row_text.center(width - 4) if center else row_text.ljust(width - 4)
            table.add_row(row_text)
        self.console.print(table)

    def table_display(self, items, width=60, fore_color="yellow"):
        headers = [header for header in items[0] if isinstance(items[0], dict)]
        table = Table(box = box.ROUNDED, width = width, style = fore_color)

        for header in headers:
            table.add_column(header)

        for item in items:
            if item == "DIVIDER":
                table.add_section()
            else:
                table.add_row(*[str(item.get(header, "")) for header in headers])
        self.console.print(table)

    def clear(self):
        self.console.clear()
