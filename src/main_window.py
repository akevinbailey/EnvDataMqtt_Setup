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
from typing import Optional, cast
from PySide6.QtCore import Slot, QByteArray
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QPlainTextEdit
)
from PySide6.QtBluetooth import (
    QBluetoothUuid, QBluetoothDeviceInfo, QLowEnergyController,
    QLowEnergyService, QLowEnergyCharacteristic
)

from device_picker import DevicePicker
from config_form import ConfigForm
from constants import SVC_UUID, CTRL_UUID, DATA_UUID, STAT_UUID

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Env Sensor Setup (Bluetooth)")
        self.resize(860, 860)

        central = QWidget(self)
        self.setCentralWidget(central)

        self.form_widget = ConfigForm(central)
        self.log = QPlainTextEdit(central)
        self.log.setReadOnly(True)
        self.log.setMaximumBlockCount(1500)

        self.btn_pick = QPushButton("Pick Device…", central)
        self.btn_connect = QPushButton("Connect", central); self.btn_connect.setEnabled(False)
        self.btn_send = QPushButton("Send Config", central); self.btn_send.setEnabled(False)
        self.btn_read_stat = QPushButton("Read Status", central); self.btn_read_stat.setEnabled(False)
        self.btn_save = QPushButton("Save Config…", central)
        self.btn_load = QPushButton("Load Config…", central)

        topbar = QHBoxLayout()
        topbar.addWidget(self.btn_pick)
        topbar.addWidget(self.btn_connect)
        topbar.addWidget(self.btn_send)
        topbar.addWidget(self.btn_read_stat)
        topbar.addStretch()
        topbar.addWidget(self.btn_load)
        topbar.addWidget(self.btn_save)

        v = QVBoxLayout(central)
        v.addLayout(topbar)
        v.addWidget(cast(QWidget,self.form_widget), 4)
        v.addWidget(QLabel("Log:", central))
        v.addWidget(self.log, 2)

        self.device_info: Optional[QBluetoothDeviceInfo] = None
        self.controller: Optional[QLowEnergyController] = None
        self.service: Optional[QLowEnergyService] = None
        self.chr_ctrl: Optional[QLowEnergyCharacteristic] = None
        self.chr_data: Optional[QLowEnergyCharacteristic] = None
        self.chr_stat: Optional[QLowEnergyCharacteristic] = None

        self.btn_pick.clicked.connect(self.on_pick_device)
        self.btn_connect.clicked.connect(self.on_connect)
        self.btn_send.clicked.connect(self.on_send)
        self.btn_read_stat.clicked.connect(self.on_read_status)
        self.btn_save.clicked.connect(self.on_save)
        self.btn_load.clicked.connect(self.on_load)

    def login(self, msg: str) -> None:
        self.log.appendPlainText(msg)

    @Slot()
    def on_save(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Save Config", "sensor_config.json", "JSON (*.json)")
        if not path: return
        try:
            import json
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.form_widget.to_dict(), f, indent=2, ensure_ascii=False)
            self.login(f"Saved config to: {path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    @Slot()
    def on_load(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Load Config", "", "JSON (*.json)")
        if not path: return
        try:
            import json
            with open(path, "r", encoding="utf-8") as f:
                d = json.load(f)
            self.form_widget.load_from_dict(d)
            self.login(f"Loaded config from: {path}")
        except Exception as e:
            QMessageBox.critical(self, "Load Error", str(e))

    @Slot()
    def on_pick_device(self) -> None:
        dlg = DevicePicker(cast(QWidget, self))
        if dlg.exec() == dlg.DialogCode.Accepted:
            sel = dlg.selected_device()
            if sel is None:
                self.login("No device selected."); return
            self.device_info = sel
            self.login(f"Selected device: {sel.name()} [{sel.address().toString()}]")
            self.btn_connect.setEnabled(True)
        else:
            self.login("Device selection canceled.")

    @Slot()
    def on_connect(self) -> None:
        if self.device_info is None:
            QMessageBox.warning(self, "No device", "Pick a device first.")
            return

        if self.controller is not None:
            self.controller.disconnectFromDevice()
            self.controller.deleteLater()
            self.controller = None

        self.login("Connecting…")
        self.controller = QLowEnergyController.createCentral(self.device_info, self)
        if self.controller is None:
            self.login("Failed to create Bluetooth controller.")
            QMessageBox.critical(self, "Bluetooth Error", "Could not create Bluetooth controller.")
            return

        self.controller.connected.connect(self._on_connected)
        self.controller.disconnected.connect(self._on_disconnected)
        self.controller.errorOccurred.connect(self._on_ctl_error)
        self.controller.serviceDiscovered.connect(self._on_service_found)
        self.controller.discoveryFinished.connect(self._on_service_scan_done)
        self.controller.connectToDevice()

    @Slot()
    def _on_connected(self) -> None:
        if self.controller is None:
            self.login("Connected signal received but controller is None."); return
        self.login("Connected. Discovering services…")
        self.controller.discoverServices()

    @Slot()
    def _on_disconnected(self) -> None:
        self.login("Disconnected.")
        self.btn_send.setEnabled(False)
        self.btn_read_stat.setEnabled(False)

    @Slot()
    def _on_ctl_error(self) -> None:
        if self.controller is None:
            self.login("Controller error but controller is None."); return
        self.login(f"Controller error: {self.controller.errorString()}")

    @Slot(QBluetoothUuid)
    def _on_service_found(self, uuid: QBluetoothUuid) -> None:
        self.login(f"Found service: {uuid.toString()}")

    @Slot()
    def _on_service_scan_done(self) -> None:
        if self.controller is None:
            self.login("Service discovery finished but controller is None."); return

        if SVC_UUID not in self.controller.services():
            self.login("Target service not found on device.")
            QMessageBox.warning(self, "Service Missing", "The target service UUID was not found.")
            return

        self.login("Target service found. Creating service client…")
        if self.service is not None:
            self.service.deleteLater()
            self.service = None

        self.service = self.controller.createServiceObject(SVC_UUID, self)
        if self.service is None:
            self.login("Failed to create service object.")
            QMessageBox.critical(self, "Bluetooth Error", "Could not create service object.")
            return

        self.service.stateChanged.connect(self._on_service_state)
        self.service.characteristicChanged.connect(self._on_chr_changed)
        self.service.errorOccurred.connect(self._on_service_error)
        self.service.discoverDetails()

    @Slot(QLowEnergyService.ServiceError)
    def _on_service_error(self, _err: QLowEnergyService.ServiceError) -> None:
        if self.service is None:
            self.login("Service error but service is None."); return
        self.login(f"Service error: {self.service.error()}")

    @Slot(QLowEnergyService.ServiceState)
    def _on_service_state(self, state: QLowEnergyService.ServiceState) -> None:
        if state != QLowEnergyService.ServiceState.ServiceDiscovered:
            return
        if self.service is None:
            self.login("Service state changed but service is None."); return

        self.login("Service discovered.")
        self.chr_ctrl = self.service.characteristic(CTRL_UUID)
        self.chr_data = self.service.characteristic(DATA_UUID)
        self.chr_stat = self.service.characteristic(STAT_UUID)

        missing = []
        if self.chr_data is None or not self.chr_data.isValid(): missing.append("DATA_UUID")
        if self.chr_ctrl is None or not self.chr_ctrl.isValid(): missing.append("CTRL_UUID")
        if self.chr_stat is None or not self.chr_stat.isValid():
            self.login("STAT_UUID not present (status read disabled).")

        if missing:
            self.login("Missing characteristics: " + ", ".join(missing))
        else:
            self.login("All characteristics present.")

        self.btn_send.setEnabled(self.chr_data is not None and self.chr_data.isValid())
        self.btn_read_stat.setEnabled(self.chr_stat is not None and self.chr_stat.isValid())

    @Slot(QLowEnergyCharacteristic, QByteArray)
    def _on_chr_changed(self, ch: QLowEnergyCharacteristic, value: QByteArray) -> None:
        if ch is None or not ch.isValid(): return
        if ch.uuid() != STAT_UUID: return
        try:
            txt = value.data().decode("utf-8", errors="replace")
        except Exception as e:
            txt = f"<decode error: {e}>"
        self.login(f"Status update: {txt}")

    @Slot()
    def on_send(self) -> None:
        if self.service is None or self.chr_data is None or not self.chr_data.isValid():
            QMessageBox.warning(self, "Not Ready", "Bluetooth service/characteristic not ready."); return

        try:
            json_str = self.form_widget.build_json()
        except Exception as e:
            QMessageBox.critical(self, "Validation Error", str(e)); return

        data = json_str.encode("utf-8")
        props = self.chr_data.properties()
        can_write = bool(props & QLowEnergyCharacteristic.PropertyType.Write)
        can_wnr   = bool(props & QLowEnergyCharacteristic.PropertyType.WriteNoResponse)
        if not (can_write or can_wnr):
            QMessageBox.warning(self, "Write Not Supported", "DATA_UUID not writable on this device."); return

        mode = (QLowEnergyService.WriteMode.WriteWithoutResponse
                if can_wnr else QLowEnergyService.WriteMode.WriteWithResponse)

        self.login(f"Writing {len(data)} bytes to DATA_UUID…")
        self.service.writeCharacteristic(self.chr_data, data, mode)
        self.login("Write requested.")

    @Slot()
    def on_read_status(self) -> None:
        if self.service is None or self.chr_stat is None or not self.chr_stat.isValid():
            return
        props = self.chr_stat.properties()
        if props & QLowEnergyCharacteristic.PropertyType.Notify:
            desc = self.chr_stat.descriptor(QBluetoothUuid.DescriptorType.ClientCharacteristicConfiguration)
            if desc.isValid():
                self.login("Enabling notifications on STAT_UUID…")
                self.service.writeDescriptor(desc, QByteArray(b"\x01\x00"))
        if props & QLowEnergyCharacteristic.PropertyType.Read:
            self.login("Reading STAT_UUID…")
            self.service.readCharacteristic(self.chr_stat)
