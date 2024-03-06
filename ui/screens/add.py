from textual import on
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Header, Footer, TabbedContent, TabPane, TextArea, RichLog
from textual.reactive import var

from ...models import Banner
from ..dialogs.info import InformationDialog

from ..dialogs.error import ErrorDialog


class AddBanner(Screen):

    banner_content = var("")
    banner_markup = var("")

    BINDINGS = [
        Binding("ctrl+s", "save_banner", "Save"),
        Binding("ctrl+x", "go_back", "Back"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.banner = Banner(content="", markedUp="")

    def compose(self):
        yield Header()
        yield TextArea.code_editor(
            text=self.banner_markup,
            id="add_textarea"
        )
        yield Footer()

    def on_mount(self):
        self.title = f"Banner #{self.banner.id}"
        text_edit: TextArea = self.query_one("#add_textarea")
        text_edit.text = self.banner.content

    @on(TextArea.Changed, "#add_textarea")
    def on_edit_textarea_changed(self, event: TextArea.Changed):
        self.banner.content = event.text_area.text

    def action_save_banner(self):
        result = self.banner.save()
        if result:
            self.app.push_screen(
                InformationDialog(
                    "[green]Banner saved[/]",
                    f"Banner #{self.banner.id} has been saved"
                )
            )
        else:
            self.app.push_screen(
                ErrorDialog(
                    "Error",
                    f"Failed to save banner #{self.banner.id}"
                )
            )

    def action_go_back(self):
        self.app.pop_screen()