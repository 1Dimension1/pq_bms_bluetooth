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
        self.cellTemperature: float = None
        self.mosfetTemperature: float = None
        self.heat: float = None
        self.protectState: str = None
        self.failureState: str = None
        self.equilibriumState: str = None
        self.batteryState: str = None
        self.SOC: float = None
        self.SOH: float = None
        self.dischargesCount: int = None
        self.dischargesAHCount: float = None

        self.firmwareVersion: str = None
        self.manfactureDate: str = None
        self.hardwareVersion: str = None

        # Human readable battery status
        self.battery_status: str = None
        self.balance_status: str = None
        self.cell_status: str = None
        self.bms_status: str = None
        self.heat_status: str = None
