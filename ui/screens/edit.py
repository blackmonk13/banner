from textual import on
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Header, Footer, TabbedContent, TabPane, TextArea, RichLog
from textual.reactive import var

from ...models import Banner
from ..dialogs.info import InformationDialog

from ..dialogs.error import ErrorDialog


class EditBanner(Screen):

    banner_id = var(0)
    banner_content = var("")
    banner_markup = var("")

    BINDINGS = [
        Binding("ctrl+s", "save_banner", "Save"),
        Binding("ctrl+e", "show_tab('edit_tab')", "Edit"),
        Binding("ctrl+p", "show_tab('preview_tab')", "Preview"),
        Binding("ctrl+q", "go_back", "Back"),
    ]

    def __init__(self, banner_id: int, **kwargs):
        super().__init__(**kwargs)
        self.banner_id = banner_id

    def compose(self):
        yield Header()
        with TabbedContent(initial="edit_tab", id="editor_tabs"):
            with TabPane("Edit", id="edit_tab"):
                yield TextArea.code_editor(text=self.banner_markup, id="edit_textarea")
            with TabPane("Preview", id="preview_tab"):
                yield RichLog(highlight=True, markup=True, id="preview_log")
        yield Footer()

    async def get_banner(self):
        banner = Banner.get(Banner.id == self.banner_id)
        if banner is not None:
            self.banner_content = banner.content
            if banner.markedUp is None or banner.markedUp == "":
                self.banner_markup = banner.content
            else:
                self.banner_markup = banner.markedUp
        else:
            self.app.push_screen(
                ErrorDialog(
                    "Error",
                    f"We could not find a banner with ID {self.banner_id}"
                )
            )

    async def on_mount(self):
        await self.get_banner()
        self.title = f"Banner #{self.banner_id}"
        text_edit: TextArea = self.query_one("#edit_textarea")
        text_preview: RichLog = self.query_one("#preview_log")
        text_edit.text = self.banner_markup
        text_preview.write(self.banner_markup)

    @on(TextArea.Changed, "#edit_textarea")
    def on_edit_textarea_changed(self, event: TextArea.Changed):
        self.banner_markup = event.text_area.text
        text_preview: RichLog = self.query_one("#preview_log")
        text_preview.clear()
        text_preview.write(event.text_area.text)

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab

    async def action_save_banner(self):
        result = (Banner.update({Banner.markedUp: self.banner_markup})
                  .where(Banner.id == self.banner_id)
                  .execute())

        if result:
            self.notify(f"Banner #{self.banner.id} has been saved")
        else:
            self.app.push_screen(
                ErrorDialog(
                    "Error", 
                    f"Failed to save banner #{self.banner_id}")
            )

    def action_go_back(self):
        self.app.pop_screen()
