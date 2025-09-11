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
from typing import Optional
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import (
    QDialog, QListWidget, QListWidgetItem, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QWidget
)
from PySide6.QtBluetooth import (
    QBluetoothDeviceInfo, QBluetoothDeviceDiscoveryAgent
)

from constants import SVC_UUID

class DevicePicker(QDialog):
    deviceSelected: Signal = Signal(QBluetoothDeviceInfo)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Select Bluetooth Device")
        self.resize(520, 380)

        self.agent = QBluetoothDeviceDiscoveryAgent(self)
        self.agent.setLowEnergyDiscoveryTimeout(8000)

        self.list = QListWidget()
        self.status = QLabel("Click 'Scan' to discover devices…")
        self.scan_btn = QPushButton("Scan")
        self.stop_btn = QPushButton("Stop"); self.stop_btn.setEnabled(False)
        self.ok_btn = QPushButton("OK"); self.ok_btn.setEnabled(False)
        self.cancel_btn = QPushButton("Cancel")

        buttons = QHBoxLayout()
        buttons.addWidget(self.scan_btn)
        buttons.addWidget(self.stop_btn)
        buttons.addStretch()
        buttons.addWidget(self.ok_btn)
        buttons.addWidget(self.cancel_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(self.list)
        layout.addWidget(self.status)
        layout.addLayout(buttons)

        self.scan_btn.clicked.connect(self.start_scan)
        self.stop_btn.clicked.connect(self.agent.stop)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.list.itemSelectionChanged.connect(self._on_sel)

        self.agent.deviceDiscovered.connect(self._on_found)
        self.agent.errorOccurred.connect(self._on_error)
        self.agent.finished.connect(self._on_finished)
        self.agent.canceled.connect(self._on_finished)

    @Slot()
    def _on_sel(self) -> None:
        self.ok_btn.setEnabled(bool(self.list.selectedItems()))

    @Slot()
    def start_scan(self) -> None:
        self.list.clear()
        self.ok_btn.setEnabled(False)
        self.status.setText("Scanning…")
        self.scan_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.agent.start(QBluetoothDeviceDiscoveryAgent.DiscoveryMethod.LowEnergyMethod)

    @Slot(QBluetoothDeviceInfo)
    def _on_found(self, info: QBluetoothDeviceInfo) -> None:
        if not (info.coreConfigurations() & QBluetoothDeviceInfo.CoreConfiguration.LowEnergyCoreConfiguration):
            return
        has_service = SVC_UUID in info.serviceUuids()
        label = f"{info.name()}  [{info.address().toString()}]"
        if has_service:
            label = "★ " + label
        item = QListWidgetItem(label)
        item.setData(int(Qt.ItemDataRole.UserRole), info)
        self.list.addItem(item)

    @Slot()
    def _on_error(self) -> None:
        self.status.setText(f"Scan error: {self.agent.errorString()}")

    @Slot()
    def _on_finished(self) -> None:
        self.scan_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status.setText("Select a device and click OK." if self.list.count() else "No Bluetooth devices found.")

    def selected_device(self) -> Optional[QBluetoothDeviceInfo]:
        item = self.list.currentItem()
        if not item:
            return None
        data = item.data(int(Qt.ItemDataRole.UserRole))
        return data if isinstance(data, QBluetoothDeviceInfo) else None

    def accept(self) -> None:
        dev = self.selected_device()
        if dev is not None:
            self.deviceSelected.emit(dev)
        super().accept()
