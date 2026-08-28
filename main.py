"""
Application entry point.

This module is the executable entry point of the
Aksara Nusantara desktop application.

Responsibilities
----------------
- Create the Qt application.
- Bootstrap the Application layer.
- Start the Qt event loop.
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from application.application import Application


def main() -> int:
    """
    Execute the application.

    Returns
    -------
    int
        Application exit code.
    """

    qt_app = QApplication(sys.argv)

    app = Application()

    app.initialize()

    app.run()

    return qt_app.exec()


if __name__ == "__main__":
    raise SystemExit(main())