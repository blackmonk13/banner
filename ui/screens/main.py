from prisma import Prisma

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header, Static, Button
from textual.reactive import var

from ..dialogs.error import ErrorDialog

from .edit import EditBanner


class Main(Screen):

    current_index = var(0)
    total_banners = var(0)
    banner_id = var(0)

    BINDINGS = [
        Binding("ctrl+e", "edit_banner", "Edit"),
        Binding("ctrl+q", "request_quit", "Quit"),
    ]

    def __init__(self, prisma: Prisma, **kwargs):
        super().__init__(**kwargs)
        self.prisma = prisma

    def compose(self) -> ComposeResult:
        yield Header(
            id="header"
        )

        yield Horizontal(
            Button("<", id="prev_btn"),
            Static(id="banner_preview"),
            Button(">", id="next_btn"),
            id="navigation",
        )
        yield Footer()

    async def update_banner_preview(self):

        if self.total_banners > 0:
            banners = await self.prisma.banners.find_many(
                skip=self.current_index,
                take=1,
            )
            banner = banners[0]
            self.banner_id = banner.id
            if banner:
                current_banner = banner.content
                self.query_one("#banner_preview").update(current_banner)
                self.title = f"Banner #{self.banner_id}"
                # self.query_one("#header").update(f"ID: {banner_id}")

    async def on_mount(self):
        if not self.prisma.is_connected():
            self.app.push_screen(
                ErrorDialog("Database not connected",
                            f"Failed to connect to the database")
            )
        else:
            self.total_banners = await self.prisma.banners.count()
            await self.update_banner_preview()

    @on(Button.Pressed, "#prev_btn")
    async def prev_banner(self) -> None:
        if self.current_index > 0:
            self.current_index -= 1
        else:
            self.current_index = self.total_banners - 1
        await self.update_banner_preview()

    @on(Button.Pressed, "#next_btn")
    async def next_banner(self) -> None:
        if self.current_index < self.total_banners - 1:
            self.current_index += 1
        else:
            self.current_index = 0
        await self.update_banner_preview()

    async def action_edit_banner(self):
        self.app.push_screen(
            EditBanner(
                prisma=self.prisma,
                banner_id=self.banner_id
            )
        )

    def action_request_quit(self):
        self.app.exit()
