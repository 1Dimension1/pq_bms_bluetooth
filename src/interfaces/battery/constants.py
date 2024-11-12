# Bluetooth characteristic for BMS data
BMS_CHARACTERISTIC_ID = '0000FFE1-0000-1000-8000-00805F9B34FB'
# characteristic for reading serial number (seems not implemented)
SN_CHARACTERISTIC_ID = "0000FFE2-0000-1000-8000-00805F9B34FB"

pq_commands = {
    'GET_VERSION':      '00 00 04 01 16 55 AA 1A',
    'GET_BATTERY_INFO': '00 00 04 01 13 55 AA 17',
    # Native application does not read internal serial number.
    # On version 1.1.4 used SN from QR code, during adding battery
    'SERIAL_NUMBER':    '00 00 04 01 10 55 AA 14'
}