from prisma import Prisma

from textual.app import App

from ..ui.screens.main import Main


class BannerApp(App):
    TITLE = "Banner"
    CSS_PATH = "../banner.tcss"

    def __init__(self, prisma: Prisma, **kwargs):
        super().__init__(**kwargs)
        self.prisma = prisma

    def on_mount(self) -> None:
        self.push_screen(Main(prisma=self.prisma))


async def run() -> None:
    """Run the application."""
    prisma = Prisma(auto_register=True)
    await prisma.connect()
    await BannerApp(prisma=prisma).run_async()
    await prisma.disconnect()
