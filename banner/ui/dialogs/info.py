"""Provides an information dialog."""

from .text import TextDialog


class InformationDialog(TextDialog):
    """Modal dialog that shows information."""

    DEFAULT_CSS = """
    InformationDialog > Vertical {
        border: thick $primary 50%;
    }
    """
