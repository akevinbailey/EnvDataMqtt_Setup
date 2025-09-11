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
from PySide6.QtGui import QValidator
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QHBoxLayout, QGroupBox, QLineEdit, QPlainTextEdit,
    QSpinBox, QRadioButton, QButtonGroup
)

from utils import make_ip_validator

class ConfigForm(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.form_layout = QFormLayout()
        self.setLayout(self.form_layout)

        # Change Bluetooth PIN?
        self.rb_change_pin_yes = QRadioButton("Yes")
        self.rb_change_pin_no = QRadioButton("No")
        self.rb_change_pin_no.setChecked(True)

        self.change_pin_group = QButtonGroup(self)
        self.change_pin_group.addButton(self.rb_change_pin_yes)
        self.change_pin_group.addButton(self.rb_change_pin_no)

        change_pin_row = QWidget(cast(QWidget, self))
        change_pin_row_l = QHBoxLayout(change_pin_row)
        change_pin_row_l.setContentsMargins(0, 0, 0, 0)
        change_pin_row_l.addWidget(self.rb_change_pin_yes)
        change_pin_row_l.addWidget(self.rb_change_pin_no)
        change_pin_row_l.addStretch()

        self.form_layout.addRow("Change Bluetooth PIN?", change_pin_row)

        self.bluetooth_group = QGroupBox("Bluetooth configuration", cast(QGroupBox, self))
        bluetooth_form = QFormLayout(self.bluetooth_group)
        bluetooth_form.setContentsMargins(9, 9, 9, 9)

        self.ed_pin = QLineEdit(); self.ed_pin.setMaxLength(6)
        bluetooth_form.addRow("Bluetooth PIN", self.ed_pin)
        self.form_layout.addRow(self.bluetooth_group)

        # Use DHCP?
        self.rb_dhcp_yes = QRadioButton("Yes")
        self.rb_dhcp_no = QRadioButton("No")
        self.rb_dhcp_yes.setChecked(True)

        self.dhcp_group = QButtonGroup(self)
        self.dhcp_group.addButton(self.rb_dhcp_yes)
        self.dhcp_group.addButton(self.rb_dhcp_no)

        dhcp_row = QWidget(cast(QWidget, self))
        dhcp_row_l = QHBoxLayout(dhcp_row)
        dhcp_row_l.setContentsMargins(0, 0, 0, 0)
        dhcp_row_l.addWidget(self.rb_dhcp_yes)
        dhcp_row_l.addWidget(self.rb_dhcp_no)
        dhcp_row_l.addStretch()

        self.form_layout.addRow("Use DHCP?", dhcp_row)

        self.ip_group = QGroupBox("Static IP configuration", cast(QGroupBox, self))
        ip_form = QFormLayout(self.ip_group)
        ip_form.setContentsMargins(9, 9, 9, 9)

        self.ed_local_ip = QLineEdit(); self.ed_local_ip.setMaxLength(15)
        self.ed_subnet   = QLineEdit(); self.ed_subnet.setMaxLength(15)
        self.ed_dns1     = QLineEdit(); self.ed_dns1.setMaxLength(15)
        self.ed_dns2     = QLineEdit(); self.ed_dns2.setMaxLength(15)
        self.ed_gateway  = QLineEdit(); self.ed_gateway.setMaxLength(15)

        v_ip = make_ip_validator()
        for w in (self.ed_local_ip, self.ed_subnet, self.ed_dns1, self.ed_dns2, self.ed_gateway):
            w.setValidator(v_ip)

        ip_form.addRow("Local IP", self.ed_local_ip)
        ip_form.addRow("Subnet", self.ed_subnet)
        ip_form.addRow("DNS 1", self.ed_dns1)
        ip_form.addRow("DNS 2", self.ed_dns2)
        ip_form.addRow("Gateway", self.ed_gateway)

        self.form_layout.addRow(self.ip_group)

        # Rest of the setup fields
        self.ed_ssid = QLineEdit(); self.ed_ssid.setMaxLength(32)
        self.ed_wifi_pwd = QLineEdit(); self.ed_wifi_pwd.setMaxLength(64); self.ed_wifi_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.ed_sensor_id = QLineEdit(); self.ed_sensor_id.setMaxLength(36)
        self.ed_cfg_name  = QLineEdit(); self.ed_cfg_name.setMaxLength(36)
        self.ed_http_url  = QLineEdit(); self.ed_http_url.setMaxLength(1024)
        self.ed_mqtt_srv  = QLineEdit(); self.ed_mqtt_srv.setMaxLength(256)

        self.sp_mqtt_port = QSpinBox(); self.sp_mqtt_port.setRange(0, 65535); self.sp_mqtt_port.setValue(1883)

        self.ed_mqtt_user = QLineEdit(); self.ed_mqtt_user.setMaxLength(24)
        self.ed_mqtt_pwd  = QLineEdit(); self.ed_mqtt_pwd.setMaxLength(1024); self.ed_mqtt_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.ed_mqtt_topic = QLineEdit(); self.ed_mqtt_topic.setMaxLength(1024)

        self.te_ca_cert = QPlainTextEdit()
        self.te_ca_cert.setPlaceholderText("Paste PEM CA certificate here… (max 3072 chars)")

        add = self.form_layout.addRow
        add("WiFi SSID", self.ed_ssid)
        add("WiFi Password", self.ed_wifi_pwd)
        add("Sensor ID", self.ed_sensor_id)
        add("Config Name", self.ed_cfg_name)
        add("HTTP Config URL", self.ed_http_url)
        add("MQTT Server", self.ed_mqtt_srv)
        add("MQTT Port", self.sp_mqtt_port)
        add("MQTT Username", self.ed_mqtt_user)
        add("MQTT Password", self.ed_mqtt_pwd)
        add("MQTT Topic", self.ed_mqtt_topic)
        add("CA Certificate (PEM)", self.te_ca_cert)

        self.rb_change_pin_no.toggled.connect(self._update_bluetooth_visibility)
        self._update_bluetooth_visibility()
        self.rb_dhcp_yes.toggled.connect(self._update_ip_visibility)
        self._update_ip_visibility()

    def _update_bluetooth_visibility(self) -> None:
        update_pin = self.rb_change_pin_no.isChecked()
        self.bluetooth_group.setVisible(not update_pin)
        if update_pin:
            self.ed_pin.clear()

    def _update_ip_visibility(self) -> None:
        use_dhcp = self.rb_dhcp_yes.isChecked()
        self.ip_group.setVisible(not use_dhcp)
        if use_dhcp:
            self.ed_local_ip.clear(); self.ed_subnet.clear()
            self.ed_dns1.clear(); self.ed_dns2.clear(); self.ed_gateway.clear()

    def build_json(self) -> str:
        use_dhcp = self.rb_dhcp_yes.isChecked()

        def is_valid_ip(widget: QLineEdit) -> bool:
            state, _, _ = widget.validator().validate(widget.text().strip(), 0)  # type: ignore[union-attr]
            return state == QValidator.State.Acceptable

        if not use_dhcp:
            for le, label in (
                (self.ed_local_ip, "localIp"),
                (self.ed_subnet,   "subnet"),
                (self.ed_dns1,     "dns1Ip"),
                (self.ed_dns2,     "dns2Ip"),
                (self.ed_gateway,  "gatewayIp"),
            ):
                txt = le.text().strip()
                if txt and not is_valid_ip(le):
                    raise ValueError(f"Invalid IPv4 address in {label}: '{txt}'")

        ca_text = self.te_ca_cert.toPlainText()
        if len(ca_text) > 3072:
            raise ValueError("CA certificate exceeds 3072 characters.")

        payload = {
            "bluetoothPin": int(self.ed_pin.text().strip()),
            "localIp": "" if use_dhcp else self.ed_local_ip.text().strip(),
            "subnet": "" if use_dhcp else self.ed_subnet.text().strip(),
            "dns1Ip": "" if use_dhcp else self.ed_dns1.text().strip(),
            "dns2Ip": "" if use_dhcp else self.ed_dns2.text().strip(),
            "gatewayIp": "" if use_dhcp else self.ed_gateway.text().strip(),
            "wifiSsid": self.ed_ssid.text().strip(),
            "wifiPassword": self.ed_wifi_pwd.text(),
            "sensorId": self.ed_sensor_id.text().strip(),
            "configName": self.ed_cfg_name.text().strip(),
            "httpConfigURL": self.ed_http_url.text().strip(),
            "mqttServer": self.ed_mqtt_srv.text().strip(),
            "mqttPort": int(self.sp_mqtt_port.value()),
            "mqttUsername": self.ed_mqtt_user.text().strip(),
            "mqttPassword": self.ed_mqtt_pwd.text(),
            "mqttTopic": self.ed_mqtt_topic.text().strip(),
            "caCertificate": ca_text,
        }
        import json
        return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)

    def to_dict(self) -> dict:
        import json
        return json.loads(self.build_json())

    def load_from_dict(self, d: dict) -> None:
        # Uses camelCase keys to match build_json()
        self.ed_pin.setText(d.get("bluetoothPin", ""))
        self.ed_local_ip.setText(d.get("localIp", ""))
        self.ed_subnet.setText(d.get("subnet", ""))
        self.ed_dns1.setText(d.get("dns1Ip", ""))
        self.ed_dns2.setText(d.get("dns2Ip", ""))
        self.ed_gateway.setText(d.get("gatewayIp", ""))

        self.ed_ssid.setText(d.get("wifiSsid", ""))
        self.ed_wifi_pwd.setText(d.get("wifiPassword", ""))
        self.ed_sensor_id.setText(d.get("sensorId", ""))
        self.ed_cfg_name.setText(d.get("configName", ""))
        self.ed_http_url.setText(d.get("httpConfigURL", ""))
        self.ed_mqtt_srv.setText(d.get("mqttServer", ""))
        self.sp_mqtt_port.setValue(int(d.get("mqttPort", 1883)))
        self.ed_mqtt_user.setText(d.get("mqttUsername", ""))
        self.ed_mqtt_pwd.setText(d.get("mqttPassword", ""))
        self.ed_mqtt_topic.setText(d.get("mqttTopic", ""))
        self.te_ca_cert.setPlainText(d.get("caCertificate", ""))

        use_dhcp = not d.get("localIp", "").strip()
        self.rb_dhcp_yes.setChecked(use_dhcp)
        self.rb_dhcp_no.setChecked(not use_dhcp)
        self._update_ip_visibility()
