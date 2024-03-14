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


class GenAsciiText(Screen[bool]):
    """Generates ASCII text."""

    fonts = ["random"] + ASCII_FONTS
    text = var("")
    art_text = var("")
    selected_font = var("random")

    banner: var[Banner | None] = var(None)

    BINDINGS = [
        Binding("ctrl+s", "save_banner", "Save"),
        Binding("ctrl+r", "regenerate", "Regenerate"),
        Binding("ctrl+q,escape", "go_back", "Back"),
    ]

    def __init__(self, text: str | None = None, **kwargs):
        super().__init__(**kwargs)
        if text is not None:
            self.text = text
        self.banner = Banner(
            content="",
            markedUp=""
        )

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
        self.title = f"Generate Ascii Text"

    @on(Select.Changed, "#font_select")
    def select_changed(self, event: Select.Changed) -> None:
        self.selected_font = str(event.value)

    @on(Input.Changed, "#input_text")
    def input_changed(self, event: Input.Changed) -> None:
        self.text = str(event.value)

    def action_regenerate(self) -> None:
        self.art_text = text2art(self.text, font=self.selected_font)

    def action_save_banner(self) -> None:
        if self.banner is not None:
            if self.banner.is_dirty():
                result = self.banner.save()
                if result:
                    self.notify(f"Banner #{self.banner.id} has been saved")
                else:
                    self.notify(
                        f"Failed to save banner #{self.banner.id}",
                        severity="error"
                    )

    @work
    async def action_go_back(self):
        if self.banner is not None:
            if self.banner.is_dirty():
                if await self.app.push_screen_wait(
                    YesNoDialog(
                        "[red bold]Save Banner Changes[/]?",
                        "You have unsaved changes. Would you like to save them?"
                    )
                ):
                    self.action_save_banner()
                    self.dismiss(True)
            else:
                if self.banner.content is not None and self.banner.content != "":
                    self.dismiss(True)
                else:
                    self.dismiss(False)

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
