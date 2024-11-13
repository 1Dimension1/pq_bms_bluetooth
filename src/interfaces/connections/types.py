import logging

logger = logging.getLogger(__name__)


class MQTTConfig:
    def __init__(self, broker, port, topic, client_id, username, password):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = client_id
        self.username = username
        self.password = password

    def log_config(self):
        logger.info("MQTT Configuration:")
        logger.info(f"Broker: {self.broker}")
        logger.info(f"Port: {self.port}")
        logger.info(f"Topic: {self.topic}")
        logger.info(f"Client ID: {self.client_id}")
        logger.info(f"Username: {self.username}")