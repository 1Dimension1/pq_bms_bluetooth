import sys
import asyncio
import logging
import argparse
import os

from interfaces.battery import BatteryInfo
from interfaces.homeassistant.mqtt import MqttClient, MQTTConfig


def commands():
    parser = argparse.ArgumentParser()
    parser.add_argument("DEVICE_MAC",
                        help="Bluetooth device MAC address in format 12:34:56:78:AA:CC",
                        type=str)

    parser.add_argument("--bms", help="Get battery BMS info", action="store_true")
    parser.add_argument("--mqtt", help="Send BMS info to MQTT server", action="store_true")
    parser.add_argument("--pair", help="Pair with device before interacting", action="store_true")
    parser.add_argument("-s", "--services", help="List device GATT services and characteristics", action="store_true")
    parser.add_argument("--verbose", help="Verbose logs", action="store_true")


    args = parser.parse_args()
    return args


def main():
    args = commands()

    logger = None
    data = None

    if args.verbose:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s [%(funcName)s] %(message)s')
        handler.setFormatter(formatter)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    try:
        battery = BatteryInfo(args.DEVICE_MAC, args.pair, logger)
    except Exception as e:
        print(f"An error occurred in BatteryInfo: {e}")

    if args.services:
        request = battery.get_request()
        asyncio.run(request.print_services())
        sys.exit(0)

    if args.bms:
        battery.read_bms()
        data = battery.get_json()
        print(data)

    if args.mqtt:
        config = MQTTConfig(
            broker=os.getenv('MQTT_BROKER'),  # Default value if env var is not set
            port=int(os.getenv('MQTT_PORT', 1883)),  # Convert to int
            topic=os.getenv('MQTT_TOPIC', 'pq_bms/data'),  # Default topic
            client_id=os.getenv('MQTT_CLIENT_ID', 'bms'),  # Default client ID
            username=os.getenv('MQTT_USERNAME', 'mqtt'),  # Default username
            password=os.getenv('MQTT_PASSWORD', '')  # Default password
        )   
        MqttClient(config, data)


if __name__ == "__main__":
    main()
