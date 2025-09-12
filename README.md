# EnvDataMqtt_Setup
## PURPOSE

A PySide6/Qt desktop utility that discovers a BLE-enabled environmental sensor and securely pushes its network and MQTT configuration (Wi-Fi, DHCP/static IP, MQTT host/port/credentials, and CA certificate) over a custom GATT service. It’s distributed under the MIT License.

## DESCRIPTION

The app provides a clean, form-based UI built with Qt widgets for all sensor settings, including a DHCP Yes/No toggle that hides or shows the static IP block as appropriate. You can save the current form to JSON and reload it later, making it easy to version and reuse configurations. A Bluetooth device picker scans for Low Energy devices and highlights ones exposing the expected service, simplifying selection before connecting.

Once connected, the tool discovers the target service and its characteristics, then writes a compact JSON payload to the device and optionally enables notifications on the status characteristic for live feedback. Windows users also get proper taskbar/title-bar icons via an explicit AppUserModelID and resource-path handling, which is compatible with bundled executables.