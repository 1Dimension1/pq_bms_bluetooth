from typing import Dict


class BatteryManagementSystem:
    def __init__(self):
        self.packVoltage: float = None
        self.voltage: float = None
        self.batteryPack: Dict[str, float] = {}
        self.current: float = None
        self.watt: float = None
        self.remainAh: float = None
        self.factoryAh: float = None
        self.cellTemperature: int = None
        self.mosfetTemperature: int = None
        self.heat: list = None
        self.protectState: list = None
        self.failureState: list = None
        self.equilibriumState: int = None
        self.batteryState: int = None
        self.SOC: int = None
        self.SOH: int = None
        self.dischargesCount: int = None
        self.dischargesAHCount: int = None

        self.firmwareVersion: str = None
        self.manfactureDate: str = None
        self.hardwareVersion: str = None

        # Human readable battery status
        self.battery_status: str = None
        self.balance_status: str = None
        self.cell_status: str = None
        self.bms_status: str = None
        self.heat_status: str = None
