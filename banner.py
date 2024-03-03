import asyncio
import os
import random
import sys
import argparse
import validators
import tempfile
import subprocess
from urllib.request import urlretrieve
from prisma import Prisma

from rich import print
from art import text2art, ASCII_FONTS

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Header, Select, Static, Button, Input
from textual.reactive import var

prisma = Prisma(auto_register=True)


def is_url(string):
    return validators.url(string)


def generate_text_art(text, font="random"):
    art_text = text2art(text, font=font)
    return art_text


async def generate_text_art(text: str, font="random"):
    class AsciiTextGen(App[str]):
        CSS_PATH = "banner.tcss"

        fonts = ["random"] + ASCII_FONTS
        i_text = var(text)
        art_text = var("")
        selected_font = var("random")

        def get_textart(self) -> str:
            self.art_text = text2art(self.i_text, font=self.selected_font)
            return self.art_text

        def compose(self) -> ComposeResult:
            yield Header()
            yield Horizontal(
                Input(
                    placeholder="Text",
                    id="input_text",
                    value=self.i_text,
                ),
                Select.from_values(
                    self.fonts,
                    id="font_select",
                    value="random",
                ),
                id="options_container"
            )
            yield Static(self.get_textart(), id="art_preview")
            yield Horizontal(
                Button("Accept", variant="primary", id="accept_btn"),
                Button("Cancel", id="cancel_btn"),
                id="btn_container",
            )

        @on(Select.Changed, "#font_select")
        def select_changed(self, event: Select.Changed) -> None:
            self.selected_font = str(event.value)
            self.query_one("#art_preview").update(self.get_textart())

        @on(Input.Changed, "#input_text")
        def input_changed(self, event: Input.Changed) -> None:
            self.i_text = str(event.value)
            self.query_one("#art_preview").update(self.get_textart())

        @on(Button.Pressed, "#accept_btn")
        def accept_pressed(self) -> None:
            self.exit(self.art_text)

        @on(Button.Pressed, "#cancel_btn")
        def cancel_pressed(self) -> None:
            self.exit(None)

    app = AsciiTextGen()
    ascii_art = await app.run_async()
    return ascii_art


async def add_banner(content: str) -> None:
    await prisma.banners.create({
        "content": content,
    })


async def delete_banner(banner_id: int) -> None:
    if not isinstance(banner_id, int) or banner_id <= 0:
        print("Invalid ID. Please provide a valid positive integer.")
        return

    await prisma.banners.delete(where={id: banner_id})


async def list_banners(page: int, page_size: int) -> None:
    banners = await prisma.banners.find_many(
        skip=(page * page_size),
        take=page_size,
    )
    for banner in banners:
        if banner.markedUp:
            print(f"ID: {banner.id}\nContent:\n{banner.markedUp}\n---\n")
        else:
            print(f"ID: {banner.id}\nContent:\n{banner.content}\n---\n")


async def get_random_banner(args):
    banners = await prisma.banners.find_many()

    if not banners:
        print("No banners found.")
        return

    random_banner = random.choice(banners)
    print(random_banner.content)


async def update_banner(banner_id: int, content: str = None, editor: str = "vim") -> None:
    if not isinstance(banner_id, int) or banner_id <= 0:
        print("Invalid ID. Please provide a valid positive integer.")
        return

    banner = await prisma.banners.find_unique(where={"id": banner_id})
    if not banner:
        print("Banner not found.")
        return

    with tempfile.NamedTemporaryFile(mode="w+t", delete=False) as tmp_file:
        tmp_file.write(banner.markedUp if banner.markedUp else banner.content)
        tmp_file.flush()

        subprocess.run([editor, tmp_file.name])

        with open(tmp_file.name, "r") as updated_file:
            updated_content = updated_file.read()

    await prisma.banners.update(where={"id": banner_id}, data={"markedUp": updated_content})


async def search_banners(keyword: str) -> None:
    banners = await prisma.banners.find_many(
        where={
            'content': {
                'contains': keyword,
                # mode: "insensitive"
            },
        },

    )

    for banner in banners:
        print(f"ID: {banner.id}\nContent:\n{banner.content}\n---\n")


async def clear_banners() -> None:
    await prisma.banners.deleteMany()


async def reset_banner_markup(banner_id: int) -> None:
    if not isinstance(banner_id, int) or banner_id <= 0:
        print("Invalid ID. Please provide a valid positive integer.")
        return

    banner = await prisma.banners.find_unique(where={"id": banner_id})
    if not banner:
        print("Banner not found.")
        return

    await prisma.banners.update(where={"id": banner_id}, data={"markedUp": None})
    print(f"Markup of banner {
          banner_id} has been reset to its original content.")


async def import_banner_from_file(file_path: str):
    if not os.path.isfile(file_path):
        print("File does not exist.")
        return

    with open(file_path, "r") as file:
        content = file.read()
        add_banner(content)
        print("Banner added from file.")


async def import_banner_from_url(url: str):
    temp_file = "temp_banner.txt"
    urlretrieve(url, temp_file)
    import_banner_from_file(temp_file)
    os.remove(temp_file)


async def export_banners(args):
    banners = await prisma.banners.find_many()

    if args.single_file:
        with open(args.file_path, "w") as file:
            separator = args.separator if args.separator else "\n---\n"
            for banner in banners:
                file.write(f"{banner.content}{separator}")
        print(f"Banners exported to {args.file_path}")
    else:
        base_name = args.base_name if args.base_name else "banner"
        extension = args.extension if args.extension else "txt"
        for i, banner in enumerate(banners, start=1):
            file_path = f"{base_name}_{i}.{extension}"
            with open(file_path, "w") as file:
                file.write(f"{banner.content}")
            print(f"Banner {i} exported to {file_path}")


async def handle_add_command(args):
    sources = args.source
    for source in sources:
        if os.path.isfile(source):
            await import_banner_from_file(source)
        elif is_url(source):
            await import_banner_from_url(source)
        else:
            if args.ascii:
                ascii_art = await generate_text_art(source)
                if ascii_art is not None:
                    await add_banner(ascii_art)
            else:
                await add_banner(source)


async def main() -> None:

    parser = argparse.ArgumentParser(
        description="Banner management application.",
    )
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser(
        "add", help="Add a new banner", aliases=["a"])
    add_parser.add_argument(
        "source", nargs="+", help="Content, file path(s), or URL(s) to add as banner(s)")
    add_parser.add_argument("--ascii", action="store_true",
                            help="Generate ASCII art from the input text")
    add_parser.set_defaults(func=handle_add_command)

    delete_parser = subparsers.add_parser(
        "delete", help="Delete a banner by ID")
    delete_parser.add_argument("id", type=int, help="Banner ID")
    delete_parser.set_defaults(func=lambda args: delete_banner(args.id))

    list_parser = subparsers.add_parser("list", help="List all banners")
    list_parser.add_argument(
        "--page", type=int, default=0, help="Page number (default: 0)")
    list_parser.add_argument("--page_size", type=int, default=10,
                             help="Number of banners per page (default: 10)")
    list_parser.set_defaults(
        func=lambda args: list_banners(args.page, args.page_size))

    random_parser = subparsers.add_parser(
        "random", help="Display a random banner")
    random_parser.set_defaults(func=get_random_banner)

    update_parser = subparsers.add_parser(
        "update", help="Update a banner by ID"
    )
    update_parser.add_argument("id", type=int, help="Banner ID")
    update_parser.add_argument(
        "--editor", default="vim", help="Editor to use for updating the banner (default: 'vim')"
    )
    update_parser.set_defaults(
        func=lambda args: update_banner(args.id, editor=args.editor))

    search_parser = subparsers.add_parser(
        "search", help="Search banners by keyword")
    search_parser.add_argument("keyword", help="Keyword to search for")
    search_parser.set_defaults(func=lambda args: search_banners(args.keyword))

    clear_parser = subparsers.add_parser("clear", help="Clear all banners")
    clear_parser.set_defaults(func=clear_banners)

    reset_parser = subparsers.add_parser(
        "reset", help="Reset the markup of a banner to its original content"
    )
    reset_parser.add_argument("id", type=int, help="Banner ID")
    reset_parser.set_defaults(func=lambda args: reset_banner_markup(args.id))

    # Export command
    export_parser = subparsers.add_parser(
        "export", help="Export banners to a file or multiple files"
    )
    export_parser.add_argument(
        "--single-file", action="store_true", help="Export all banners to a single file"
    )
    export_parser.add_argument(
        "--separator", default=None, help="Separator between banners in a single file (default: '\\n---\\n')"
    )
    export_parser.add_argument(
        "--base-name", default=None, help="Base name for multiple files (default: 'banner')"
    )
    export_parser.add_argument(
        "--extension", default=None, help="Extension for multiple files (default: 'txt')"
    )
    export_parser.add_argument(
        "file_path", nargs="?", help="Path to the file where you want to export the banners")
    export_parser.set_defaults(func=export_banners)

    args = parser.parse_args()

    if not hasattr(args, "func"):

        parser.print_help()
        sys.exit(1)

    await prisma.connect()

    await args.func(args)
    await prisma.disconnect()


if __name__ == "__main__":
    asyncio.run(main())


# python banner.py add "Hello, World!"
# python banner.py add /path/to/banner.txt
# python banner.py add http://example.com/banner.txt
# python banner.py add "Hello, World!" --ascii
# python banner.py list --page 1 --page_size 10
# python banner.py random
# python banner.py search keyword
# python banner.py clear
# python banner.py export --single-file --separator "\n===\n" output.txt
# python banner.py export --base-name "my_banner" --extension "md"
# python banner.py update 1 --editor nano
# python banner.py reset 1
