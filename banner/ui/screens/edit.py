from textual import on, work
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Header, Footer, TabbedContent, TabPane, TextArea, RichLog
from textual.reactive import var

from ...models import Banner
from ..dialogs import InformationDialog, ErrorDialog, YesNoDialog

# TODO: Allow editing of original content along with markup


class EditBanner(Screen[bool]):

    banner_id: var[int | None] = var(None)
    banner_content = var("")
    banner_markup: var[str | None] = var(None)

    initial_markup = var("")

    banner: var[Banner | None] = var(None)

    BINDINGS = [
        Binding("ctrl+s", "save_banner", "Save"),
        Binding("ctrl+e", "show_tab('edit_tab')", "Edit"),
        Binding("ctrl+p", "show_tab('preview_tab')", "Preview"),
        Binding("ctrl+q,escape", "go_back", "Back"),
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

    def on_mount(self):
        self.title = f"Editing Banner #{self.banner_id}"
        text_edit: TextArea = self.query_one("#edit_textarea")
        text_preview: RichLog = self.query_one("#preview_log")
        text_edit.text = self.banner_markup
        text_preview.write(self.banner_markup)

        # Save the initial markup
        self.initial_markup = self.banner_markup

    @on(TextArea.Changed, "#edit_textarea")
    def on_edit_textarea_changed(self, event: TextArea.Changed):
        self.banner_markup = event.text_area.text
        text_preview: RichLog = self.query_one("#preview_log")
        text_preview.clear()
        text_preview.write(event.text_area.text)

        self.banner.markedUp = event.text_area.text

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab

    def action_save_banner(self):
        if self.banner is not None:
            if self.banner.is_dirty():
                result = self.banner.save()
                if result:
                    self.notify(f"Banner #{self.banner_id} has been saved")
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
                # Get the current markup
                current_markup = self.banner_markup

                # Check if the current markup is different from the initial markup
                if current_markup != self.initial_markup:
                    # If the markup has been changed during the current editing session, dismiss with True
                    self.dismiss(True)
                else:
                    # If the markup has not been changed during the current editing session, dismiss with False
                    self.dismiss(False)
    

    def watch_banner_id(self, banner_id: int | None):
        if banner_id is not None:
            banner = Banner.get(Banner.id == self.banner_id)
            if banner is not None:
                self.banner = banner
            else:
                self.notify(
                    f"We could not find a banner with ID {self.banner_id}",
                    severity="error"
                )
                self.dismiss(False)

    def watch_banner(self, banner: Banner | None):
        if banner is not None:
            if banner.markedUp is None or banner.markedUp == "":
                self.banner_markup = banner.content
            else:
                self.banner_markup = banner.markedUp
