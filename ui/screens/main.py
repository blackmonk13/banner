
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Static, Button, RichLog
from textual.reactive import var

from ...models import Banner

from .edit import EditBanner
from .add import AddBanner


class Main(Screen):
    current_index = var(1)
    total_banners = var(0)
    banner_id = var(0)

    BINDINGS = [
        Binding("ctrl+a", "add_banner", "Add"),
        Binding("ctrl+e", "edit_banner", "Edit"),
        Binding("ctrl+x", "request_quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(
            id="header"
        )

        yield Horizontal(
            Button("<", id="prev_btn"),
            RichLog(highlight=True, markup=True, id="banner_preview"),
            Button(">", id="next_btn"),
            id="navigation",
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
        if self.current_index > 1:
            self.current_index -= 1
        else:
            self.current_index = self.total_banners
        self.update_banner_preview()

    @on(Button.Pressed, "#next_btn")
    def next_banner(self) -> None:
        if self.current_index < self.total_banners:
            self.current_index += 1
        else:
            self.current_index = 1
        self.update_banner_preview()

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

    def action_request_quit(self):
        self.app.exit()
