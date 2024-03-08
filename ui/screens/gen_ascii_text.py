from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Footer, Header, Static, Button, RichLog, Select, Input
from textual.reactive import var

from art import text2art, ASCII_FONTS

from ..dialogs import YesNoDialog, ErrorDialog

from ...models import Banner


class GenAsciiText(Screen):
    """Generates ASCII text."""

    fonts = ["random"] + ASCII_FONTS
    text = var("")
    art_text = var("")
    selected_font = var("random")

    BINDINGS = [
        Binding("ctrl+s", "save_banner", "Save"),
        Binding("ctrl+r", "regenerate", "Regenerate"),
        Binding("ctrl+q", "go_back", "Back"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.banner = Banner(content="", markedUp="")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Horizontal(
                Input(
                    placeholder="Text",
                    id="input_text",
                    value=self.text,
                ),
                Select.from_values(
                    self.fonts,
                    id="font_select",
                    value="random",
                ),
                id="options_container"
            ),
            RichLog(
                highlight=True,
                markup=True,
                id="banner_preview"
            ),
            id="generate_container"
        )
        yield Footer()

    def on_mount(self):
        self.title = f"Banner #{self.banner.id}"
        # self.banner.content = self.get_textart()

    @on(Select.Changed, "#font_select")
    def select_changed(self, event: Select.Changed) -> None:
        self.selected_font = str(event.value)

    @on(Input.Changed, "#input_text")
    def input_changed(self, event: Input.Changed) -> None:
        self.text = str(event.value)

    def action_regenerate(self) -> None:
        self.art_text = text2art(self.text, font=self.selected_font)

    def action_save_banner(self) -> None:
        result = self.banner.save()
        if result:
            self.notify(f"Banner #{self.banner.id} has been saved")
            self.app.pop_screen()
        else:
            self.app.push_screen(
                ErrorDialog(
                    "Error",
                    f"Failed to save banner #{self.banner.id}"
                )
            )

    def action_go_back(self) -> None:
        self.app.pop_screen()

    def watch_text(self, text: str) -> None:
        self.art_text = text2art(text, font=self.selected_font)

    def watch_selected_font(self, selected_font: str) -> None:
        self.art_text = text2art(self.text, font=selected_font)
            
    def watch_art_text(self, art_text: str) -> None:
        self.update_preview(art_text)
        self.banner.content = art_text
        
    def get_textart(self, text: str) -> str:
        art_text = text2art(text, font=self.selected_font)
        return art_text

    def update_preview(self, content: str) -> None:
        try:
            banner_preview: RichLog = self.query_one("#banner_preview")
            banner_preview.clear()
            banner_preview.write(content)
        except:
            pass
