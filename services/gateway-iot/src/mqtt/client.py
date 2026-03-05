import json
import logging
from typing import Callable

import paho.mqtt.client as mqtt

from src.config import settings

LOGGER = logging.getLogger(__name__)


class MQTTGatewayClient:
    def __init__(self, on_payload: Callable[[str, dict], bool]) -> None:
        self._on_payload = on_payload
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(settings.mqtt_user, settings.mqtt_password)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client: mqtt.Client, *_args) -> None:
        client.subscribe("casa/#")
        client.subscribe("jardim/#")
        LOGGER.info("Connected to MQTT and subscribed to casa/#, jardim/#")

    def _on_message(
        self, _client: mqtt.Client, _userdata, msg: mqtt.MQTTMessage
    ) -> None:
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            self._on_payload(msg.topic, payload)
        except Exception as exc:  # noqa: BLE001
            LOGGER.exception("Error processing MQTT message: %s", exc)

    def start(self) -> None:
        self.client.connect(
            settings.mqtt_host, settings.mqtt_port, settings.mqtt_keepalive
        )
        self.client.loop_start()

    def stop(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
