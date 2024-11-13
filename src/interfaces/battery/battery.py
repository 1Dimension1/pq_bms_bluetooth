import json
import asyncio
import logging

from interfaces.bluetooth.request import BluetoothRequest
from .constants import BMS_CHARACTERISTIC_ID, pq_commands
from .types import BatteryManagementSystem


class BatteryInfo:
    '''
    Class parse BMS information from PowerQueen LiFePO4 battery over bluetooth

    Attributes:
        logger (str): Instance of python logger.
    '''

    def __init__(self, 
                 bluetooth_device_mac: str,
                 pair_device: bool = False,
                 logger=None):
        
        self.bms = BatteryManagementSystem()

        if logger:
            self._logger = logger
        else:
            self._logger = logging.getLogger(__name__)

        try:
            self._request = BluetoothRequest(
                bluetooth_device_mac,
                pair_device=pair_device,
                logger=self._logger
            )
        except Exception as e:
            self._logger.error("Failed to initialize Request: %s", e)
            raise

    def get_request(self):
        '''
          Return Blutooth request instance
        '''
        return self._request

    def read_bms(self):
        '''
          Function read BMS info via bluetooth using bleak client
        '''
        asyncio.run(self._request.bulk_send(
            characteristic_id=BMS_CHARACTERISTIC_ID,
            commands_parsers={
                pq_commands["GET_VERSION"]: self.parse_version,
                pq_commands["GET_BATTERY_INFO"]: self.parse_battery_info,
                # Internal SN not used or not implemented
                # self.pq_commands["SERIAL_NUMBER"]: self.parse_serial_number
            }
        ))

    def get_json(self):
        '''
          Function return complete JSON string of parsed BMS information
        '''
        state = self.__dict__
        del state['_logger']
        del state['_request']

        return json.dumps(
            state,
            default=lambda o: o.__dict__,
            sort_keys=False,
            indent=4)

    def parse_battery_info(self, data):
        '''
          Parse battery info from bytearray
        '''
        self.bms.packVoltage = int.from_bytes(data[8:12][::-1], byteorder='big')
        self.bms.voltage = int.from_bytes(data[12:16][::-1], byteorder='big')

        cell = 1
        batPack = data[16:48]
        for key, dt in enumerate(batPack):
            if not dt or key % 2:
                continue

            cellVoltage = int.from_bytes([batPack[key + 1], dt], byteorder='big')
            self.bms.batteryPack[cell] = cellVoltage/1000
            cell += 1

        # Load \ Unload current A
        current = int.from_bytes(data[48:52][::-1], byteorder='big', signed=True)
        self.bms.current = round(current / 1000, 2)

        # Calculated load \ unload Watt
        self.bms.watt = round((self.bms.voltage * +current) / 10000, 1) / 100

        # Remain Ah
        remainAh = int.from_bytes(data[62:64][::-1], byteorder='big')
        self.bms.remainAh = round(remainAh/100, 2)

        # Factory Ah
        fccAh = int.from_bytes(data[64:66][::-1], byteorder='big')
        self.bms.factoryAh = round(fccAh/100, 2)

        # Temperature
        self.bms.cellTemperature = int.from_bytes(data[52:54][::-1], byteorder='big')
        self.bms.mosfetTemperature = int.from_bytes(data[54:56][::-1], byteorder='big')

        self.bms.heat = list(data[68:72][::-1])

        self.bms.protectState = list(data[76:80][::-1])
        self.bms.failureState = list(data[80:84][::-1])
        self.bms.equilibriumState = int.from_bytes(data[84:88][::-1], byteorder='big')
        self.bms.batteryState = int.from_bytes(data[88:90][::-1], byteorder='big')

        # Charge level
        self.bms.SOC = int.from_bytes(data[90:92][::-1], byteorder='big')

        # Battery Status ??
        self.bms.SOH = int.from_bytes(data[92:96][::-1], byteorder='big')

        self.bms.dischargesCount = int.from_bytes(data[96:100][::-1], byteorder='big')

        # Discharge AH times
        self.bms.dischargesAHCount = int.from_bytes(data[100:104][::-1], byteorder='big')

        # Additional human readable statuses
        self.bms.battery_status = self.get_battery_status()

        if self.bms.equilibriumState > 0:
            self.bms.balance_status = "Battery cells are being balanced for better performance."
        else:
            self.bms.balance_status = "All cells are well-balanced."

        if self.bms.failureState[0] > 0 or self.bms.failureState[1] > 0:
            self.bms.cell_status = "Fault alert! There may be a problem with cell."
        else:
            self.bms.cell_status = "Battery is in optimal working condition."

    def parse_version(self, data):
        '''
          Parse firmware version from bytearray
        '''
        start = data[8:]
        self.bms.firmwareVersion = (f"{int.from_bytes(start[0:2][::-1], byteorder='big')}"
                                f".{int.from_bytes(start[2:4][::-1], byteorder='big')}"
                                f".{int.from_bytes(start[4:6][::-1], byteorder='big')}")
        self.bms.manfactureDate = (f"{int.from_bytes(start[6:8][::-1], byteorder='big')}"
                               f"-{int(start[8])}"
                               f"-{int(start[9])}")

        vers = ""
        # rawV = data[0:8]
        for ver in start[0::2]:
            if 32 <= ver <= 126:
                vers += chr(ver)

        self.bms.hardwareVersion = vers

    def parse_serial_number(self, data):
        '''
          Parse battery serial number from bytearray
          Seems logic not implemented in BMS
        '''
        print(f"Serial number: ${data}")

    def get_battery_status(self) -> str:
        '''
          Return human readable battery status
        '''
        status = ''
        if self.bms.current == 0:
            status = "Standby"
        elif self.bms.current > 0:
            status = "Charging"
        elif self.bms.current < 0:
            status = "Discharging"

        if self.bms.SOC >= 100 or self.bms.batteryState == 4:
            status = "Fully charged"

        return status
