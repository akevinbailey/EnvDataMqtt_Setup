#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  Copyright (c) 2025. Andrew Kevin Bailey
#  This code, firmware, and software is released under the MIT License (http://opensource.org/licenses/MIT).
#
#  The MIT License (MIT)
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or significant portions of
#  the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#  BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.\

import os, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from main_window import MainWindow
from utils import resource_path, set_app_user_model_id

def main() -> None:
    set_app_user_model_id("EnvDataMqtt_Setup")  # harmless on non-Windows
    app = QApplication(sys.argv)

    ico_path = resource_path("../resources/EnvDataMqtt_Setup.ico")
    png_path = resource_path("../resources/EnvDataMqtt_Setup.png")

    if sys.platform == "win32" and os.path.exists(ico_path):
        app.setWindowIcon(QIcon(ico_path))
    elif os.path.exists(png_path):
        app.setWindowIcon(QIcon(png_path))

    w = MainWindow()
    if sys.platform == "win32" and os.path.exists(ico_path):
        w.setWindowIcon(QIcon(ico_path))
    elif os.path.exists(png_path):
        w.setWindowIcon(QIcon(png_path))
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()