from os import path
import argparse
import os
import aiohttp
from typing import List
import validators
import tempfile
from peewee import *

from rich import print
from rich.progress import track
from rich.prompt import Confirm

from art import text2art, ASCII_FONTS

from textual.app import App
from textual import on, work

from ..ui.screens import Main, AddBanner, EditBanner, GenAsciiText
from ..models import app_db, Banner


class BannerApp(App):
    TITLE = "Banner"
    DEFAULT_CSS = """
    Screen {
    align: center top;
    layers: below above;
    }

    #carousel_container, #generate_container {
    align: center top;
    width: 100%;
    height: 100%;
    }

    #navigation, #options_container {
    width: 100%;
    height: 3;
    layout: grid;
    
    grid-gutter: 1;
    }

    #navigation {
    dock: bottom;
    grid-size: 2 1;
    }

    #banner_preview {
    width: 100%;
    }

    #prev_btn {
    dock: left;
    }

    #next_btn {
    dock: right;
    }

    #prev_btn, #next_btn {
    background: #2e2e2e;
    }

    #editor_tabs, #edit_tabs, #preview_tab {
    width: 100%;
    }

    #options_container {
    dock: top;
    grid-size: 4 1;
    }

    #font_select {
    # width: 30%;
    height: 100%;
    }

    #input_text {
    # width: 70%;
    height: 100%;
    column-span: 3;
    }
    """

    def __init__(self, cli_args: argparse.Namespace) -> None:
        """Initialise the application.

        Args:
            cli_args: The command line arguments.
        """
        super().__init__()
        self._args = cli_args

    async def on_mount(self) -> None:
        self.push_screen(Main())  # Push the Main screen first
        if self._args.command == "edit":
            # TODO: Make the edit command have multiediting and do the editing in sequence possibly with 'push_screen_wait'
            self.push_screen(
                EditBanner(
                    banner_id=self._args.id
                )
            )


def create_tables() -> None:
    all_models = [Banner,]
    with app_db:
        app_db.create_tables(
            all_models
        )


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="banner",
        description="Banner management application.",
    )

    subparsers = parser.add_subparsers(dest="command")

    """Add subcommand"""
    add_parser = subparsers.add_parser(
        "add", help="Add a new banner",)
    add_parser.add_argument(
        "source", nargs="+",
        help="Content, file path(s), or URL(s) to add as banner(s)"
    )
    add_parser.add_argument(
        "--ascii",
        action="store_true",
        help="Generate ASCII art from the input text"
    )
    add_parser.add_argument(
        "--font",
        default="random",
        choices=ASCII_FONTS,
        help="Font to use for ASCII art. Use 'random' to choose a random font."
    )
    add_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated ASCII text to the console instead of adding it as a banner"
    )

    """Delete subcommand"""
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a banner by ID"
    )
    delete_parser.add_argument(
        "id",
        type=int,
        help="Banner ID"
    )

    """Edit subcommand"""
    edit_parser = subparsers.add_parser(
        "edit",
        help="Edit a banner by ID"
    )
    edit_parser.add_argument(
        "id",
        type=int,
        help="Banner ID"
    )

    """Reset subcommand"""
    reset_parser = subparsers.add_parser(
        "reset",
        help="Reset the markup of a banner to its original content"
    )
    reset_parser.add_argument(
        "id",
        type=int,
        help="Banner ID"
    )

    """Show subcommand"""
    show_parser = subparsers.add_parser(
        "show",
        help="Show a banner by ID or a random banner"
    )
    show_parser.add_argument(
        "id_or_random",
        help="Banner ID or 'random' to show a random banner"
    )
    show_parser.add_argument(
        "--content-only",
        action="store_true",
        help="Print the content of the banner rather than the markup"
    )

    """Export subcommand"""
    export_parser = subparsers.add_parser(
        "export",
        help="Export banners to a file or multiple files"
    )
    export_parser.add_argument(
        "--single-file",
        action="store_true",
        help="Export all banners to a single file"
    )
    export_parser.add_argument(
        "--separator",
        default=None,
        help="Separator between banners in a single file (default: '\\n---\\n')"
    )
    export_parser.add_argument(
        "--base-name",
        default=None,
        help="Base name for multiple files (default: 'banner')"
    )
    export_parser.add_argument(
        "--extension",
        default=None,
        help="Extension for multiple files (default: 'txt')"
    )
    export_parser.add_argument(
        "file_path",
        nargs="?",
        help="Path to the file where you want to export the banners"
    )

    # Finally, parse the command line.
    return parser.parse_args()


def is_url(string):
    return validators.url(string)


def gen_ascii_text(text: str, font: str = "random"):
    art_text = text2art(text, font=font)
    return art_text


def import_banner_from_file(file_path: str) -> str | None:
    if not os.path.isfile(file_path):
        print(
            f"File '{file_path}' does not exist."
        )
        return None

    with open(file_path, "r") as file:
        content = file.read()
        return content


async def import_banner_from_url(url: str) -> str | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
                return content
    except aiohttp.ClientError as e:
        print(
            f"Error importing banner from URL '{url}': {e}"
        )
        return None


async def get_source_content(source: str) -> str | None:
    if os.path.isfile(source):
        content = import_banner_from_file(source)
    elif is_url(source):
        content = await import_banner_from_url(source)
    else:
        content = source
    return content


def export_banners(args: argparse.Namespace) -> None:
    banners = Banner.select()
    num_banners = len(banners)

    if args.single_file:
        file_path = args.file_path or f"banners.{'txt' if not args.extension else args.extension}"
        with open(file_path, "w") as f:
            for banner in banners:
                f.write(banner.content)
                f.write(args.separator or "\n---\n")

        print(f"Exported {num_banners} banners to {path.abspath(file_path)}")
    else:
        base_name = args.base_name or "banner"
        extension = args.extension or "txt"
        for i, banner in enumerate(banners, start=1):
            file_path = f"{base_name}_{i}.{extension}"
            with open(file_path, "w") as f:
                f.write(banner.content)

            print(f"Exported banner {i} to {path.abspath(file_path)}")


async def add_banners(
    sources: List[str],
    ascii: bool,
    dry_run: bool,
    font: str
) -> tuple[int, int, List[str]]:
    num_succeeded = 0
    num_failed = 0
    dry_run_content: List[str] = []

    for source in track(sources, description="Adding banners"):
        content = await get_source_content(source)
        if content is None:
            num_failed += 1
            continue
        if ascii:
            # TODO: Add to generated ascii text markup field
            # and the raw content to the content field then
            # in the edit screen users could generate ascii text if they're
            # not happy with the initial result
            # or let the user pick a font in the arguments
            content = gen_ascii_text(content, font=font)
        if dry_run:
            dry_run_content.append(content)
        else:
            try:
                banner = Banner.create(content=content)
                num_succeeded += 1
            except Exception as e:
                print(f"Failed to add banner: {e}")
                num_failed += 1

    return num_succeeded, num_failed, dry_run_content


def delete_banner(banner_id: int) -> None:
    """Delete a banner by ID."""
    if Confirm.ask(f"Are you sure you want to delete banner #{banner_id}?"):
        result = Banner.delete().where(Banner.id == banner_id).execute()
        if result:
            print(f"Banner #{banner_id} has been deleted")
        else:
            print("Failed to delete banner")


def show_banner(id_or_random: str, content_only: bool = False) -> None:
    """Show a single banner based on its ID or a random banner."""
    if id_or_random == "random":
        banner = Banner.select().order_by(fn.Random()).limit(1).get()
    else:
        banner = Banner.get_by_id(int(id_or_random))

    if banner:
        if content_only:
            print(banner.content)
        else:
            if banner.markedUp is None or banner.markedUp == "":
                print(banner.content)
            else:
                print(banner.markedUp)
    else:
        print("Banner not found")


def reset_banner(banner_id: int) -> None:
    banner = Banner.get_by_id(banner_id)
    if banner:
        banner.markup = banner.content
        banner.save()
        print(f"Banner #{banner_id} has been reset")
    else:
        print("Banner not found")


async def run() -> None:
    """Run the application."""
    app_db.connect(reuse_if_open=True)
    create_tables()
    cli_args = get_args()

    if cli_args.command == "add":
        sources = cli_args.source
        num_succeeded, num_failed, dry_run_content = await add_banners(
            sources,
            cli_args.ascii,
            cli_args.dry_run,
            cli_args.font
        )
        if not cli_args.dry_run:
            print(
                f"Added {num_succeeded} banners. {num_failed} failed."
            )
        else:
            for content in dry_run_content:
                print(content)
    elif cli_args.command == "delete":
        delete_banner(cli_args.id)
    elif cli_args.command == "show":
        show_banner(cli_args.id_or_random, cli_args.content_only)
    elif cli_args.command == "reset":
        reset_banner(cli_args.id)
    elif cli_args.command == "export":
        export_banners(cli_args)
    else:
        await BannerApp(cli_args).run_async()

    app_db.close()
