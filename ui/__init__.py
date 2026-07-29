"""
User Interface Layer.

This package contains the graphical user interface components of
the Aksara Nusantara desktop application.
"""

from .main_window import MainWindow
from .workspace import Workspace

__all__ = [
    "MainWindow",
    "Workspace",
]