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
#  SOFTWARE.

from __future__ import annotations
import os, sys
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

def make_ip_validator() -> QRegularExpressionValidator:
    rx = QRegularExpression(r"^(\d{1,3}\.){3}\d{1,3}$")
    return QRegularExpressionValidator(rx)

def resource_path(name: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.abspath(""))
    return os.path.join(base, name)

def set_app_user_model_id(app_id: str) -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes
        sh = getattr(ctypes, "windll", None)
        if not sh or not hasattr(sh, "shell32"):
            return
        fn = getattr(sh.shell32, "SetCurrentProcessExplicitAppUserModelID", None)
        if not fn:
            return
        try:
            from ctypes import HRESULT, c_wchar_p
            fn.restype = HRESULT
            fn.argtypes = [c_wchar_p]
        except Exception as e:
            sys.stderr.write(f"Error in {app_id} setting app ID: {e}\n")
        fn("EnvDataMqtt_Setup")
    except Exception as e:
        sys.stderr.write(f"Error in {app_id} setting app ID: {e}\n")
