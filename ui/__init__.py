"""
User Interface Layer.

This package contains the graphical user interface components of
the Aksara Nusantara desktop application.
"""

from .central_workspace import CentralWorkspace
from .main_window import MainWindow

__all__ = [
    "CentralWorkspace",
    "MainWindow",
]