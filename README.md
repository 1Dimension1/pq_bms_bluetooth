# pq_bms_bluetooth
Python library for PowerQueen LiFePO4 batteries with BMS Bluetooth connection.

The code does not make any changes or change any settings in BMS of battery. Only reading information.

## Installation

Clone and create python virtual environment

```
git clone https://github.com/dmytro-tsepilov/pq_bms_bluetooth.git
cd ./pq_bms_bluetooth
python -m venv venv
source venv/bin/activate
```

Install requirements

```
pip install -r requirements.txt
```

## Usage

Find Bluetooth MAC address of your battery.
On linux it possible to do with `bluez` tool.

Start bluetooth tool `bluetoothctl` and scan for avaliable bluetooth devices `scan on`.
<br>Once it find some devices and shows the list, stop scanning with command `scan off`

<span style="color:blue">[bluetooth]</span># scan on
<br>Discovery started
<br>[<span style="color:yellow">CHG</span>] Controller 12:34:56:78:AA:CC Discovering: yes
<br>[<span style="color:green">NEW</span>] Device 12:34:56:78:CC:12 Some Sound Device etc.
<br>[<span style="color:green">NEW</span>] Device 12:34:56:78:29:CF P-12100BXXX77-A00123
<br>[<span style="color:green">NEW</span>] Device 12:34:56:78:F8:7C 12-33-44-55-F8-7C
<br>[<span style="color:green">NEW</span>] Device 12:34:56:78:D4:3D 33-44-55-EE-D4-3D
<br><span style="color:blue">[bluetooth]</span># scan off

## CLI

```
# python main.py --help
usage: main.py [-h] [--bms] [-s] [--verbose] DEVICE_MAC

positional arguments:
  DEVICE_MAC      Bluetooth device MAC address in format 12:34:56:78:AA:CC

options:
  -h, --help      show this help message and exit
  --bms           Get battery BMS info
  -s, --services  List device GATT services
  --verbose       Verbose logs
```

### Examples

Get BMS information
```
# python main.py 12:34:56:78:AA:CC --bms
{
    "packVoltage": 12793,
    "voltage": 13338,
    "batteryPack": {
        "1": 3.335,
        "2": 3.335,
        "3": 3.335,
        "4": 3.333
    },
    "current": 0,
    "remianAh": 105.0,
    "factoryAh": 105.0,
    "cellTemperature": 25,
    "mosfetTemperature": 26,
    "heat": 72,
    "protectState": 0,
    "failureState": 0,
    "equilibriumState": 0,
    "batteryState": 4,
    "SOC": "100%",
    "SOH": "105%",
    "dischargesCount": 0,
    "dischargesAHCount": 101,
    "firmwareVersion": "1.4.0",
    "manfactureDate": "1980-01-01",
    "hardwareVersion": "T12345678"
}
```


## Tested on

Software:
- Python 3.10, 3.11
- Linux Ubuntu 22.04
- Raspberry Pi OS Debian 12 (bookworm) (kernel 6.6+)

Hardware:
- Power Queen LiFePO4 12V 100A
