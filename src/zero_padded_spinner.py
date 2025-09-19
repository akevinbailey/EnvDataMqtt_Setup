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

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QSpinBox, QLineEdit
from typing import cast, Any

class ZeroPaddedSpinBox(QSpinBox):
    def __init__(self, digits: int = 6, parent=None):
        super().__init__(parent)
        self._digits = int(digits)
        self.setRange(0, 10**self._digits - 1)
        self.setKeyboardTracking(False)

        # Right-aligned editor. NOTE: no maxLength — we normalize ourselves.
        le = self.lineEdit() or QLineEdit(self)
        le.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setLineEdit(le)

        # Keep the display padded and react to both user edits & programmatic changes
        self.valueChanged.connect(self._sync_display_from_value)
        cast(Any, le.textEdited).connect(self._on_text_edited)
        self._sync_display_from_value(self.value())

    # --- formatting/parsing helpers ---
    def textFromValue(self, value: int) -> str:
        return f"{int(value):0{self._digits}d}"

    @staticmethod
    def _digits_only(s: str) -> str:
        return "".join(ch for ch in s if ch.isdigit())

    # --- slots ---
    @Slot(int)
    def _sync_display_from_value(self, v: int):
        t = self.textFromValue(v)
        le = self.lineEdit()
        le.blockSignals(True)
        le.setText(t)
        le.setCursorPosition(len(t))  # keep caret at right
        le.blockSignals(False)

    @Slot(str)
    def _on_text_edited(self, s: str):
        # Keep last N digits that the user typed and zero-pad on the left
        ds = self._digits_only(s)[-self._digits:]
        v = int(ds) if ds else 0

        # Update value (clamped to range) without recursive signals
        self.blockSignals(True)
        self.setValue(v)
        self.blockSignals(False)

        # Refresh padded view
        self._sync_display_from_value(v)