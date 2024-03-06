from peewee import *

from textual.app import App

from ..ui.screens.main import Main
from ..models import app_db, Banner


class BannerApp(App):
    TITLE = "Banner"
    CSS_PATH = "../banner.tcss"

    def on_mount(self) -> None:
        self.push_screen(Main())


def create_tables() -> None:
    all_tables = [Banner,]
    with app_db:
        app_db.create_tables(
            [tbl for tbl in all_tables if (lambda x: x.table_exists())(tbl)]
        )


async def run() -> None:
    """Run the application."""
    app_db.connect(reuse_if_open=True)
    create_tables()
    await BannerApp().run_async()
    app_db.close()
