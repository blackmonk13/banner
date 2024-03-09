
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Footer, Header, Static, Button, RichLog
from textual.reactive import var

from ..dialogs.yes_or_no import YesNoDialog

from ...models import Banner

from .edit import EditBanner
from .add import AddBanner
from .gen_ascii_text import GenAsciiText


class Main(Screen):
    current_index = var(1)
    total_banners = var(0)
    banner_id = var(0)

    BINDINGS = [
        Binding("ctrl+a,ctrl+i,insert", "add_banner", "Add"),
        Binding("ctrl+e", "edit_banner", "Edit"),
        Binding("ctrl+g", "gen_ascii_text_banner", "Gen. ASCII Text"),
        Binding("ctrl+d,delete", "delete_banner", "Delete"),
        Binding("ctrl+q,escape", "request_quit", "Quit"),
        Binding("left,up", "navigate(0)", "", show=False),
        Binding("right,down", "navigate(1)", "", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header(
            id="header"
        )
        yield Container(
            RichLog(highlight=True, markup=True, id="banner_preview"),
            Horizontal(
                Button("<", id="prev_btn"),
                Button(">", id="next_btn"),
                id="navigation",
            ),
            id="carousel_container"
        )
        yield Footer()

    def update_banner_preview(self):
        self.total_banners = Banner.select().count()
        if self.total_banners > 0:
            banners = Banner.select().order_by(Banner.id).paginate(
                self.current_index,
                1,
            )
            banner = banners[0]
            self.banner_id = banner.id
            if banner:
                if banner.markedUp is None or banner.markedUp == "":
                    current_banner = banner.content
                else:
                    current_banner = banner.markedUp

                banner_preview: RichLog = self.query_one("#banner_preview")
                banner_preview.clear()
                banner_preview.write(current_banner)
                self.title = f"Banner #{self.banner_id}"

    def on_mount(self):
        self.update_banner_preview()

    @on(Button.Pressed, "#prev_btn")
    def prev_banner(self) -> None:
        self.go_to_previous()

    def go_to_previous(self):
        if self.current_index > 1:
            self.current_index -= 1
        else:
            self.current_index = self.total_banners
        self.update_banner_preview()

    @on(Button.Pressed, "#next_btn")
    def next_banner(self) -> None:
        self.go_to_next()

    def go_to_next(self):
        if self.current_index < self.total_banners:
            self.current_index += 1
        else:
            self.current_index = 1
        self.update_banner_preview()

    def action_navigate(self, direction: int):
        if direction > 0:
            self.go_to_next()
        else:
            self.go_to_previous()

    def action_add_banner(self):
        self.app.push_screen(
            AddBanner()
        )

    def action_edit_banner(self):
        self.app.push_screen(
            EditBanner(
                banner_id=self.banner_id
            )
        )

    @work
    async def action_delete_banner(self):
        if await self.app.push_screen_wait(
            YesNoDialog(
                "[red bold]Delete Banner[/]",
                """
                Are you sure you want to delete this banner?\n
                [yellow1 bold italic]This action cannot be undone.[/]
                """
            ),
        ):
            result = Banner.delete().where(Banner.id == self.banner_id).execute()
            if result:
                self.notify(f"Banner #{self.banner_id} has been deleted")
                self.go_to_previous()
            else:
                self.notify("Failed to delete banner", severity="error")

    def action_gen_ascii_text_banner(self):
        self.app.push_screen(
            GenAsciiText()
        )
        
    def action_request_quit(self):
        self.app.exit()
