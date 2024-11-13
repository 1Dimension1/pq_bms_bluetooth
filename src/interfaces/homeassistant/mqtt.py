import json
import logging

from paho.mqtt.client import Client as mqtt_client
from paho.mqtt.enums import CallbackAPIVersion
from .types import MQTTConfig

logger = logging.getLogger(__name__)


class MqttClient:
    def __init__(self, config: MQTTConfig, data: str):
        self.config = config
        self.data = data

        self.client = mqtt_client(CallbackAPIVersion.VERSION2,
                                  client_id=config.client_id,
                                  clean_session=True)

        self.client.username_pw_set(config.username, config.password)

        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            self.client.enable_logger()

        self.client.on_connect = self.on_connect

        self.connect()
        self.client.loop_forever()

    def connect(self):
        self.client.connect(self.config.broker, self.config.port)
        logger.info(f'Connecting to {self.config.broker}:{self.config.port}')

    def publish(self, topic, payload):
        logger.info(f'Publishing to {topic}')

        self.client.publish(topic, payload)

        logger.info('Message published')
        logger.debug(payload)

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"Connected with result code {rc}")
        if rc == 0:
            self.publish(f"{self.config.topic}/data", json.dumps(self.data))
            logger.info("Message published to:", f"{self.config.topic}/data")
        else:
            logger.error(f"Connection failed with result code {rc}")

    def on_publish(self, client, userdata, mid):
        logger.info(f"Message published with mid: {mid}")
        self.client.disconnect()
